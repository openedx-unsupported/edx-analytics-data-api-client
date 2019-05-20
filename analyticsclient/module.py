from __future__ import absolute_import

import six

from analyticsclient.base import BaseEndpoint
from analyticsclient.constants import data_formats


class Module(BaseEndpoint):
    """Module related analytics data."""

    def __init__(self, client, course_id, module_id):
        """
        Initialize the Module client.

        Arguments:
            client (analyticsclient.client.Client): The client to use to access the API.
            course_id (str): String identifying the course
            module_id (str): String identifying the module
        """
        super(Module, self).__init__(client)
        self.course_id = six.text_type(course_id)
        self.module_id = six.text_type(module_id)

    def answer_distribution(self, data_format=data_formats.JSON):
        """
        Get answer distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = 'problems/{0}/answer_distribution/'.format(self.module_id)

        return self.client.get(path, data_format=data_format)

    def grade_distribution(self, data_format=data_formats.JSON):
        """
        Get grade distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = 'problems/{0}/grade_distribution/'.format(self.module_id)

        return self.client.get(path, data_format=data_format)

    def sequential_open_distribution(self, data_format=data_formats.JSON):
        """
        Get open distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = 'problems/{0}/sequential_open_distribution/'.format(self.module_id)

        return self.client.get(path, data_format=data_format)

    def video_timeline(self, data_format=data_formats.JSON):
        """
        Get video segments/timeline for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = 'videos/{0}/timeline/'.format(self.module_id)

        return self.client.get(path, data_format=data_format)
