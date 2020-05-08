from __future__ import absolute_import

from analyticsclient.constants import data_formats, http_methods


class BaseEndpoint:
    """Base class for endpoints that use a client object."""

    def __init__(self, client):
        """
        Initialize the API client.

        Arguments:
            client (analyticsclient.client.Client): The client to use to access remote resources.
        """
        self.client = client


class PostableCourseIDsEndpoint(BaseEndpoint):
    """Base class for endpoints that pass in course IDs with either GET or POST."""

    path = None  # Override in subclass
    max_num_ids_for_get = 10  # Optionally override in subclass

    def do_request(self, course_ids, data, data_format=data_formats.JSON):
        """
        Given course IDs, do the appropriate request method (GET or POST).

        Arguments:
            course_ids (list[str]): A list of course IDs to pass in
            data (dict): Arguments for endpoint, sans course IDs
            data_format (data_format)

        Returns: dict
        """
        data_with_ids = data.copy()
        if course_ids:
            data_with_ids.update(course_ids=course_ids)
        method = (
            http_methods.POST
            if len(course_ids or []) > self.max_num_ids_for_get
            else http_methods.GET
        )
        return self.client.request(method, self.path, data=data_with_ids, data_format=data_format)
