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
        super().__init__(client)
        self.course_id = str(course_id)
        self.module_id = str(module_id)

    def answer_distribution(self, data_format=data_formats.JSON):
        """
        Get answer distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = f'problems/{self.module_id}/answer_distribution/'

        return self.client.get(path, data_format=data_format)

    def grade_distribution(self, data_format=data_formats.JSON):
        """
        Get grade distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = f'problems/{self.module_id}/grade_distribution/'

        return self.client.get(path, data_format=data_format)

    def sequential_open_distribution(self, data_format=data_formats.JSON):
        """
        Get open distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = f'problems/{self.module_id}/sequential_open_distribution/'

        return self.client.get(path, data_format=data_format)

    def video_timeline(self, data_format=data_formats.JSON):
        """
        Get video segments/timeline for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = f'videos/{self.module_id}/timeline/'

        return self.client.get(path, data_format=data_format)
