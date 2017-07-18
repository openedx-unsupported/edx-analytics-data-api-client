import analyticsclient.constants.data_format as DF


class CourseAggregateData(object):

    def __init__(self, client):
        self.client = client

    def course_aggregate_data(self, course_ids=None, data_foromat=DF.JSON):
        post_data = (
            {'course_ids': course_ids} if course_ids
            else {}
        )
        path = 'course_aggregate_data/'
        return self.client.post(path, post_data=post_data, data_format=data_format)
