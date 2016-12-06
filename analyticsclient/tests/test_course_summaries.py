import httpretty


from analyticsclient.tests import ClientTestCase


class CourseSummariesTests(ClientTestCase):

    def setUp(self):
        super(CourseSummariesTests, self).setUp()
        self.base_uri = self.get_api_url('course_summaries/')
        self.course_summaries_client = self.client.course_summaries()
        httpretty.enable()

    @httpretty.activate
    def test_all_summaries_url(self):
        """Course summaries can be called without parameters."""
        httpretty.register_uri(httpretty.GET, self.base_uri, body='{}')
        self.course_summaries_client.course_summaries()

    @httpretty.activate
    def test_courses_ids(self):
        """Course summaries can be called with course IDs"""

        def register_uri(course_ids):
            httpretty.reset()
            uri_template = '{uri}?course_ids={ids}'
            uri = uri_template.format(uri=self.base_uri, ids=course_ids)
            httpretty.register_uri(httpretty.GET, uri, body='{}')

        course_ids = ['edx/demo/course', 'another/demo/course']

        register_uri([course_ids[0]])
        self.course_summaries_client.course_summaries(course_ids=[course_ids[0]])

        register_uri(course_ids)
        self.course_summaries_client.course_summaries(course_ids=course_ids)

    @httpretty.activate
    def test_fields(self):
        """Course summaries can be called with fields."""

        def register_uri(fields):
            httpretty.reset()
            uri_template = '{uri}?fields={fields}'
            uri = uri_template.format(uri=self.base_uri, fields=fields[0])
            httpretty.register_uri(httpretty.GET, uri, body='{}')

        fields = ['course_id', 'enrollment_modes']
        register_uri([fields[0]])
        self.course_summaries_client.course_summaries(fields=[fields[0]])

        register_uri(fields)
        self.course_summaries_client.course_summaries(fields=fields)

    @httpretty.activate
    def test_all_parameters(self):
        """Course summaries can be called with both fields and course IDs."""

        def register_uri(course_ids, fields):
            httpretty.reset()
            uri_template = '{uri}?course_ids={ids}fields={fields}'
            uri = uri_template.format(uri=self.base_uri, ids=course_ids, fields=fields)
            httpretty.register_uri(httpretty.GET, uri, body='{}')

        course_ids = ['edx/demo/course', 'another/demo/course']
        fields = ['course_id', 'enrollment_modes']
        register_uri(course_ids, fields)
        self.course_summaries_client.course_summaries(course_ids=course_ids, fields=fields)
