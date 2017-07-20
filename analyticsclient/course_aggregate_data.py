from analyticsclient.constants import MAX_NUM_COURSE_IDS_FOR_GET
import analyticsclient.constants.data_format as DF


class CourseAggregateData(object):

    PATH = 'course_aggregate_data/'

    def __init__(self, client):
        self.client = client

    def course_aggregate_data(self, course_ids=None, data_format=DF.JSON):
        data = (
            {'course_ids': course_ids} if course_ids
            else {}
        )
        request_method = (
            self.client.post
            if len(course_ids or []) > MAX_NUM_COURSE_IDS_FOR_GET
            else self.client.get
        )
        return request_method(self.PATH, data=data, data_format=data_format)
