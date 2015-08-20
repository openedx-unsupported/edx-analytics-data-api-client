import logging

import requests
import requests.exceptions
from analyticsclient.constants import data_format as DF

from analyticsclient.course import Course
from analyticsclient.exceptions import ClientError, InvalidRequestError, NotFoundError, TimeoutError
from analyticsclient.module import Module
from analyticsclient.status import Status
from analyticsclient.users import User


log = logging.getLogger(__name__)


class Client(object):
    """
    Analytics API client.

    The instance has attributes like `status` and `courses` that provide access to instances of
    :class: `~analyticsclient.status` and :class: `~analyticsclient.course`. This is the preferred (and only supported)
    way to get access to those classes and their methods.
    """

    # Date/time formats to be used when sending and parsing data from the API
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = DATE_FORMAT + 'T%H%M%S'

    def __init__(self, base_url, auth_token=None, timeout=0.25):
        """
        Initialize the client.

        Arguments:
            base_url (str): URL of the API server (e.g. http://analytics.edx.org/api/v0)
            auth_token (str): Authentication token
            timeout (number): Maximum number of seconds during which all requests musts complete
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.timeout = timeout

        self.status = Status(self)
        self.courses = lambda course_id: Course(self, course_id)
        self.users = lambda username: User(self, username)
        self.modules = lambda course_id, module_id: Module(self, course_id, module_id)

    def get(self, resource, timeout=None, data_format=DF.JSON):
        """
        Retrieve the data for a resource.

        Arguments:

            resource (str): Path in the form of slash separated strings.
            timeout (float): Continue to attempt to retrieve a resource for this many seconds before giving up and
                raising an error.
            data_format (str): Format in which data should be returned

        Returns: API response data in specified data_format

        Raises: ClientError if the resource cannot be retrieved for any reason.

        """
        response = self._request(resource, timeout=timeout, data_format=data_format)

        if data_format == DF.CSV:
            return response.text

        try:
            return response.json()
        except ValueError:
            message = 'Unable to decode JSON response'
            log.exception(message)
            raise ClientError(message)

    def has_resource(self, resource, timeout=None):
        """
        Check if the server responds with a 200 OK status code when the resource is requested.

        Inherited from `Client`.

        Arguments:

            resource (str): Path in the form of slash separated strings.
            timeout (float): Continue to attempt to retrieve a resource for this many seconds before giving up and
                raising an error.

        Returns: True iff the resource exists.

        """
        try:
            self._request(resource, timeout=timeout)
            return True
        except ClientError:
            return False

    # pylint: disable=no-member
    def _request(self, resource, timeout=None, data_format=DF.JSON):
        if timeout is None:
            timeout = self.timeout

        accept_format = 'application/json'
        if data_format == DF.CSV:
            accept_format = 'text/csv'

        headers = {
            'Accept': accept_format,
        }

        if self.auth_token:
            headers['Authorization'] = 'Token ' + self.auth_token

        try:
            uri = '{0}/{1}'.format(self.base_url, resource)
            response = requests.get(uri, headers=headers, timeout=timeout)

            status = response.status_code
            if status != requests.codes.ok:
                message = 'Resource "{0}" returned status code {1}'.format(resource, status)
                error_class = ClientError

                if status == requests.codes.bad_request:
                    message = 'The request to {0} was invalid.'.format(uri)
                    error_class = InvalidRequestError
                elif status == requests.codes.not_found:
                    message = 'Resource {0} was not found on the API server.'.format(uri)
                    error_class = NotFoundError

                log.error(message)
                raise error_class(message)

            return response

        except requests.exceptions.Timeout:
            message = "Response from {0} exceeded timeout of {1}s.".format(resource, timeout)
            log.exception(message)
            raise TimeoutError(message)

        except requests.exceptions.RequestException:
            message = 'Unable to retrieve resource'
            log.exception(message)
            raise ClientError('{0} "{1}"'.format(message, resource))
