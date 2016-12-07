import ddt
import httpretty


from analyticsclient.tests import ClientTestCase


@ddt.ddt
class CourseSummariesTests(ClientTestCase):

    def setUp(self):
        super(CourseSummariesTests, self).setUp()
        self.base_uri = self.get_api_url('course_summaries/')
        self.course_summaries_client = self.client.course_summaries()
        httpretty.enable()

    def verify_last_querystring_equal(self, expected_query):
        """
        Convenience method for asserting the last request was made with the
        expected query parameters.
        """
        self.assertDictEqual(httpretty.last_request().querystring, expected_query)

    def expected_query(self, course_ids=None, fields=None):
        """Packs the query arguments into expected format for http pretty."""
        query = {}
        for field, data in zip(['course_ids', 'fields'], [course_ids, fields]):
            if data is not None:
                query[field] = [','.join(data)]
        return query

    @httpretty.activate
    def test_all_summaries_url(self):
        """Course summaries can be called without parameters."""
        httpretty.register_uri(httpretty.GET, self.base_uri, body='{}')
        self.course_summaries_client.course_summaries()

    @httpretty.activate
    @ddt.data(
        ['edx/demo/course'],
        ['edx/demo/course', 'another/demo/course']
    )
    def test_courses_ids(self, course_ids):
        """Course summaries can be called with course IDs"""
        uri_template = '{uri}?course_ids={ids}'
        uri = uri_template.format(uri=self.base_uri, ids=course_ids)
        httpretty.register_uri(httpretty.GET, uri, body='{}')
        self.course_summaries_client.course_summaries(course_ids=course_ids)
        self.verify_last_querystring_equal(self.expected_query(course_ids=course_ids))

    @httpretty.activate
    @ddt.data(
        ['course_id'],
        ['course_id', 'enrollment_modes']
    )
    def test_fields(self, fields):
        """Course summaries can be called with fields."""
        uri_template = '{uri}?fields={fields}'
        uri = uri_template.format(uri=self.base_uri, fields=fields[0])
        httpretty.register_uri(httpretty.GET, uri, body='{}')
        self.course_summaries_client.course_summaries(fields=fields)
        self.verify_last_querystring_equal(self.expected_query(fields=fields))

    @httpretty.activate
    @ddt.data(
        (['edx/demo/course'], ['course_id']),
        (['edx/demo/course', 'another/demo/course'], ['course_id', 'enrollment_modes'])
    )
    @ddt.unpack
    def test_all_parameters(self, course_ids, fields):
        """Course summaries can be called with both fields and course IDs."""
        httpretty.reset()
        uri_template = '{uri}?course_ids={ids}fields={fields}'
        uri = uri_template.format(uri=self.base_uri, ids=course_ids, fields=fields)
        httpretty.register_uri(httpretty.GET, uri, body='{}')
        self.course_summaries_client.course_summaries(course_ids=course_ids, fields=fields)
        self.verify_last_querystring_equal(self.expected_query(course_ids=course_ids, fields=fields))
