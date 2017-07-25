from analyticsclient.constants import http_methods, MAX_NUM_COURSE_IDS_FOR_GET
import analyticsclient.constants.data_format as DF


class CourseSummaries(object):
    """Course summaries."""

    PATH = 'course_summaries/'

    def __init__(self, client):
        """
        Initialize the CourseSummaries client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.

        """
        self.client = client

    def course_summaries(
            self,
            course_ids=None,
            availability=None,
            pacing_type=None,
            program_ids=None,
            text_search=None,
            sort_key=None,
            order=None,
            page=None,
            page_size=None,
            fields=None,
            exclude=None,
            data_format=DF.JSON,
        ):
        """
        Get list of summaries.

        Arguments:
            course_ids: Array of course IDs as strings to return.  Default is to return all.
            fields: Array of fields to return.  Default is to return all.
            exclude: Array of fields to exclude from response. Default is to not exclude any fields.
            programs: If included in the query parameters, will include the programs array in the response.
        """
        method = (
            http_methods.POST
            if len(course_ids or []) > MAX_NUM_COURSE_IDS_FOR_GET
            else http_methods.GET
        )
        raw_data = {
            'course_ids': course_ids,
            'availability': availability,
            'pacing_type': pacing_type,
            'program_ids': program_ids,
            'text_search': text_search,
            'sortKey': sort_key,
            'order': order,
            'page': page,
            'page_size': page_size,
            'fields': fields,
            'exclude': exclude,
        }
        data = {
            key: value
            for key, value in raw_data.iteritems()
            if value
        }
        return self.client.request(method, self.PATH, data=data, data_format=data_format)
