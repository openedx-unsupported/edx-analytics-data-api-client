from analyticsclient.constants import http_methods, MAX_NUM_COURSE_IDS_FOR_GET
import analyticsclient.constants.data_format as DF


class CourseAggregateData(object):

    PATH = 'course_aggregate_data/'

    def __init__(self, client):
        self.client = client

    def course_aggregate_data(self, course_ids=None, data_format=DF.JSON):
        method = (
            http_methods.POST
            if len(course_ids or []) > MAX_NUM_COURSE_IDS_FOR_GET
            else http_methods.GET
        )
        data = (
            {'course_ids': course_ids} if course_ids
            else {}
        )
        return self.client.request(method, self.PATH, data=data, data_format=data_format)
