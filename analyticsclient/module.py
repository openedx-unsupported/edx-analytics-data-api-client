import urllib

import analyticsclient.constants.data_format as DF


class Module(object):
    """Module related analytics data."""

    def __init__(self, client, course_id, module_id):
        """
        Initialize the Module client.

        Arguments:
            client (analyticsclient.client.Client): The client to use to access the API.
            course_id (str): String identifying the course
            module_id (str): String identifying the module
        """
        self.client = client
        self.course_id = unicode(course_id)
        self.module_id = unicode(module_id)

    def answer_distribution(self, data_format=DF.JSON, consolidate_variants=False):
        """
        Get answer distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
            consolidate_variants (bool): Consolidate erroneously random answers (default is False)
        """
        params = {
            'consolidate_variants': consolidate_variants,
        }

        querystring = urllib.urlencode(params)
        path = 'problems/{0}/answer_distribution/?{1}'.format(self.module_id, querystring)

        return self.client.get(path, data_format=data_format)

    def grade_distribution(self, data_format=DF.JSON):
        """
        Get grade distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = 'problems/{0}/grade_distribution/'.format(self.module_id)

        return self.client.get(path, data_format=data_format)

    def sequential_open_distribution(self, data_format=DF.JSON):
        """
        Get open distribution data for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = 'problems/{0}/sequential_open_distribution/'.format(self.module_id)

        return self.client.get(path, data_format=data_format)

    def video_timeline(self, data_format=DF.JSON):
        """
        Get video segments/timeline for a module.

        Arguments:
            data_format (str): Format in which to return data (default is JSON)
        """
        path = 'videos/{0}/timeline/'.format(self.module_id)

        return self.client.get(path, data_format=data_format)
