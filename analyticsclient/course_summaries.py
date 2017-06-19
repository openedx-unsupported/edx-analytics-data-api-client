import analyticsclient.constants.data_format as DF


class CourseSummaries(object):
    """Course summaries."""

    def __init__(self, client):
        """
        Initialize the CourseSummaries client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.

        """
        self.client = client

    def course_summaries(self, course_ids=None, fields=None, exclude=None, programs=None, data_format=DF.JSON):
        """
        Get list of summaries.

        Arguments:
            course_ids: Array of course IDs as strings to return.  Default is to return all.
            fields: Array of fields to return.  Default is to return all.
            exclude: Array of fields to exclude from response. Default is to not exclude any fields.
            programs: If included in the query parameters, will include the programs array in the response.
        """
        post_data = {}
        for param_name, data in zip(['course_ids', 'fields', 'exclude', 'programs'],
                                    [course_ids, fields, exclude, programs]):
            if data:
                post_data[param_name] = data

        path = 'course_summaries/'

        return self.client.post(path, post_data=post_data, data_format=data_format)
