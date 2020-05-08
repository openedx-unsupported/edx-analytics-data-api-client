from __future__ import absolute_import

import logging

import requests
import requests.exceptions

from analyticsclient.constants import data_formats, http_methods
from analyticsclient.course import Course
from analyticsclient.course_summaries import CourseSummaries
from analyticsclient.course_totals import CourseTotals
from analyticsclient.engagement_timeline import EngagementTimeline
from analyticsclient.exceptions import ClientError, InvalidRequestError, NotFoundError, TimeoutError  # pylint: disable=redefined-builtin
from analyticsclient.module import Module
from analyticsclient.programs import Programs
from analyticsclient.status import Status

log = logging.getLogger(__name__)


class Client:
    """
    Analytics API client.

    The instance has attributes `status` and `courses` that provide access to instances of
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
            base_url (str): URL of the API server (e.g. http://analytics.edx.org/api/v1)
            auth_token (str): Authentication token
            timeout (number): Maximum number of seconds during which all requests musts complete
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.timeout = timeout

        self.status = Status(self)
        self.course_summaries = lambda: CourseSummaries(self)
        self.course_totals = lambda: CourseTotals(self)
        self.programs = lambda: Programs(self)
        self.courses = lambda course_id: Course(self, course_id)
        self.modules = lambda course_id, module_id: Module(self, course_id, module_id)
        self.engagement_timeline = lambda username, course_id: EngagementTimeline(self, username, course_id)

    def get(self, *args, **kwargs):
        """
        Retrieve the data for a resource.

        Equivalent to `request(http_methods.GET, ...)`

        Returns: API response data in specified data_format

        Raises: ClientError if the resource cannot be retrieved for any reason.
        """
        return self.request(http_methods.GET, *args, **kwargs)

    def request(self, method, resource, data=None, timeout=None, data_format=data_formats.JSON):
        """
        Retrieve the from an HTTP request.

        Arguments:

            method (http_method): HTTP method. Only GET and POST are supported currenly.
            resource (str): Path in the form of slash separated strings.
            data (dict): Dictionary containing POST data.
            timeout (float): Continue to attempt to retrieve a resource for this many seconds before giving up and
                raising an error.
            data_format (str): Format in which data should be returned

        Returns: API response data in specified data_format

        Raises: ClientError if the resource cannot be retrieved for any reason.

        """
        response = self._request(
            method=method,
            resource=resource,
            data=data,
            timeout=timeout,
            data_format=data_format
        )

        if data_format == data_formats.CSV:
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
            self._request(http_methods.GET, resource, timeout=timeout)
            return True
        except ClientError:
            return False

    # pylint: disable=no-member
    def _request(self, method, resource, data=None, timeout=None, data_format=data_formats.JSON):
        if timeout is None:
            timeout = self.timeout

        accept_format = 'application/json'
        if data_format == data_formats.CSV:
            accept_format = 'text/csv'

        headers = {
            'Accept': accept_format,
        }

        if self.auth_token:
            headers['Authorization'] = 'Token ' + self.auth_token

        try:
            uri = '{0}/{1}'.format(self.base_url, resource)

            if method == http_methods.GET:
                params = self._data_to_get_params(data or {})
                response = requests.get(uri, params=params, headers=headers, timeout=timeout)
            elif method == http_methods.POST:
                response = requests.post(uri, data=(data or {}), headers=headers, timeout=timeout)
            else:
                raise ValueError(
                    'Invalid \'method\' argument: expected {0} or {1}, got {2}'.format(
                        http_methods.GET,
                        http_methods.POST,
                        method,
                    )
                )

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

    @staticmethod
    def _data_to_get_params(data):
        return {
            key: (
                ','.join(value)
                if isinstance(value, list)
                else str(value)
            )
            for key, value in data.items()
        }
