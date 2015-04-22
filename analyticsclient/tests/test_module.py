import json

import httpretty

from analyticsclient.tests import ClientTestCase


class ModulesTests(ClientTestCase):
    def setUp(self):
        super(ModulesTests, self).setUp()
        httpretty.enable()

        self.course_id = 'edX/TestX/TestCourse'
        self.module_id = 'i4x://TestCourse/block1/module2/abcd1234'

        self.module = self.client.modules(self.course_id, self.module_id)

    def tearDown(self):
        super(ModulesTests, self).tearDown()
        httpretty.disable()

    def test_open_distribution_url(self):
        """ Verifies that the sequential open URL is correct. """
        uri = self.get_api_url('problems/{0}/sequential_open_distribution/'.format(self.module_id))

        httpretty.register_uri(httpretty.GET, uri, body='{}')
        self.module.sequential_open_distribution()

    def test_answer_distribution_url(self):
        """ Verifies that the answer distribution URL is correct. """
        uri = self.get_api_url('problems/{0}/answer_distribution/'.format(self.module_id))

        httpretty.register_uri(httpretty.GET, uri, body='{}')
        self.module.answer_distribution()

    def test_grade_distribution_url(self):
        """ Verifies that the grade distribution URL is correct. """
        uri = self.get_api_url('problems/{0}/grade_distribution/'.format(self.module_id))

        httpretty.register_uri(httpretty.GET, uri, body='{}')
        self.module.grade_distribution()

    @httpretty.activate
    def test_open_distribution_response(self):
        """ Verifies that open distribution responds with the expected values. """
        body = [
            {
                'course_id': self.course_id,
                'module_id': self.module_id,
                'count': 123,
                'created': '2014-01-01T00:00:00Z'
            }
        ]

        uri = self.get_api_url('problems/{0}/sequential_open_distribution/'.format(self.module_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.module.sequential_open_distribution())

    @httpretty.activate
    def test_answer_distribution_response(self):
        """ Verifies that answer distribution responds with the expected values. """
        body = [
            {
                'course_id': self.course_id,
                'module_id': self.module_id,
                'part_id': self.module_id.replace('/', '-') + '-part1',
                'correct': True,
                'first_response_count': 2,
                'last_response_count': 2,
                'value_id': 'choice_4',
                'answer_value_text': 'User chose this answer.',
                'answer_value_numeric': None,
                'variant': 123,
                'created': "2014-01-01T00:01:00"
            }
        ]

        uri = self.get_api_url('problems/{0}/answer_distribution/'.format(self.module_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.module.answer_distribution())

    @httpretty.activate
    def test_grade_distribution_response(self):
        """ Verifies that the grade distribution responds with the expected values. """
        body = [
            {
                'module_id': self.module_id,
                'course_id': self.course_id,
                'grade': 0,
                'max_grade': 1,
                'count': 1,
                'created': '2014-01-01T00:01:00'
            }
        ]

        uri = self.get_api_url('problems/{0}/grade_distribution/'.format(self.module_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.module.grade_distribution())

    @httpretty.activate
    def test_video_timeline_response(self):
        """ Verifies that the video timeline responds with the expected values. """
        body = [
            {
                'segment': 0,
                'num_users': 140,
                'num_views': 64234,
                'created': '2014-01-01T00:01:00'
            }
        ]

        uri = self.get_api_url('videos/{0}/timeline/'.format(self.module_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.module.video_timeline())
