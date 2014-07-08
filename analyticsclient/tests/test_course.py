import json

import httpretty

from analyticsclient.tests import ClientTestCase


class CoursesTests(ClientTestCase):
    def setUp(self):
        super(CoursesTests, self).setUp()
        self.course_id = 'edX/DemoX/Demo_Course'
        self.course = self.client.courses(self.course_id)
        httpretty.enable()

    def tearDown(self):
        super(CoursesTests, self).tearDown()
        httpretty.disable()

    def test_recent_active_user_count(self):
        body = {
            u'course_id': u'edX/DemoX/Demo_Course',
            u'interval_start': u'2014-05-24T00:00:00Z',
            u'interval_end': u'2014-06-01T00:00:00Z',
            u'activity_type': u'any',
            u'count': 300,
        }

        uri = self.get_api_url('courses/{0}/recent_activity'.format(self.course_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertDictEqual(body, self.course.recent_active_user_count)

    def assertEnrollmentResponseData(self, course, data, demographic=None):
        uri = self.get_api_url('courses/{0}/enrollment'.format(course.course_id))
        if demographic:
            uri += '/%s' % demographic
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(data))
        self.assertDictEqual(data, course.enrollment(demographic))

    def test_recent_problem_activity_count(self):
        body = {
            u'course_id': u'edX/DemoX/Demo_Course',
            u'interval_start': u'2014-05-24T00:00:00Z',
            u'interval_end': u'2014-06-01T00:00:00Z',
            u'activity_type': u'attempted_problem',
            u'count': 200,
        }

        uri = self.get_api_url('courses/{0}/recent_activity?activity_type=attempted_problem'.format(self.course_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertDictEqual(body, self.course.recent_problem_activity_count)

    def test_enrollment_birth_year(self):
        data = {
            u'birth_years': {
                u'1894': 13,
                u'1895': 19
            }
        }
        self.assertEnrollmentResponseData(self.course, data, 'birth_year')

    def test_enrollment_education(self):
        data = {
            u'education_levels': {
                u'none': 667,
                u'junior_secondary': 6051,
                u'primary': 981,
                u'associates': 12255,
                u'bachelors': 70885,
                u'masters': 53216,
                u'doctorate': 9940,
                u'other': 5722,
                u'secondary': 51591
            }
        }

        self.assertEnrollmentResponseData(self.course, data, 'education')

    def test_enrollment_gender(self):
        data = {
            u'genders': {
                u'm': 133240,
                u'o': 423,
                u'f': 77495
            }
        }
        self.assertEnrollmentResponseData(self.course, data, 'gender')
