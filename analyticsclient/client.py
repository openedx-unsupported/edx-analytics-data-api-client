import logging

import requests
import requests.exceptions

from analyticsclient.course import Course
from analyticsclient.exceptions import ClientError
from analyticsclient.status import Status


log = logging.getLogger(__name__)


class Client(object):
    """
    Analytics API client

    The instance has attributes `status` and `courses` that provide access to instances of
    :class: `~analyticsclient.status` and :class: `~analyticsclient.course`. This is the preferred (and only supported)
    way to get access to those classes and their methods.
    """
    def __init__(self, base_url, auth_token=None):
        """
        Initialize the client.

        Arguments:
            base_url (str): URL of the API server (e.g. http://analytics.edx.org/api/v0)
            auth_token (str): Authentication token
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.timeout = 0.1

        self.status = Status(self)
        self.courses = lambda course_id: Course(self, course_id)

    def get(self, resource, timeout=None):
        """
        Retrieve the data for a resource.

        Arguments:

            resource (str): Path in the form of slash separated strings.
            timeout (float): Continue to attempt to retrieve a resource for this many seconds before giving up and
                raising an error.

        Returns: A structure consisting of simple python types (dict, list, int, str etc).

        Raises: ClientError if the resource cannot be retrieved for any reason.

        """
        response = self._request(resource, timeout=timeout)

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

    def _request(self, resource, timeout=None):
        if timeout is None:
            timeout = self.timeout

        headers = {
            'Accept': 'application/json',
        }
        if self.auth_token:
            headers['Authorization'] = 'Token ' + self.auth_token

        try:
            response = requests.get('{0}/{1}'.format(self.base_url, resource), headers=headers, timeout=timeout)

            if response.status_code != requests.codes.ok:  # pylint: disable=no-member
                message = 'Resource "{0}" returned status code {1}'.format(resource, response.status_code)
                log.error(message)
                raise ClientError(message)

            return response

        except requests.exceptions.RequestException:
            message = 'Unable to retrieve resource'
            log.exception(message)
            raise ClientError('{0} "{1}"'.format(message, resource))
