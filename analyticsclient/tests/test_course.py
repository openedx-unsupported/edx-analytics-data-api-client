import json

import httpretty
from analyticsclient import activity_type as at
from analyticsclient import demographic as demo

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

    def assertEnrollmentResponseData(self, course, data, demographic=None):
        uri = self.get_api_url('courses/{0}/enrollment/'.format(course.course_id))
        if demographic:
            uri += '%s/' % demographic
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(data))
        self.assertDictEqual(data, course.enrollment(demographic))

    def assertRecentActivityResponseData(self, course, activity_type):
        body = {
            u'course_id': unicode(course.course_id),
            u'interval_start': u'2014-05-24T00:00:00Z',
            u'interval_end': u'2014-06-01T00:00:00Z',
            u'activity_type': unicode(activity_type),
            u'count': 200,
        }

        uri = self.get_api_url('courses/{0}/recent_activity/?activity_type={1}'.format(self.course_id, activity_type))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertDictEqual(body, self.course.recent_activity(activity_type))

    def test_enrollment_birth_year(self):
        data = {
            u'birth_years': {
                u'1894': 13,
                u'1895': 19
            }
        }
        self.assertEnrollmentResponseData(self.course, data, demo.BIRTH_YEAR)

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

        self.assertEnrollmentResponseData(self.course, data, demo.EDUCATION)

    def test_enrollment_gender(self):
        data = {
            u'genders': {
                u'm': 133240,
                u'o': 423,
                u'f': 77495
            }
        }
        self.assertEnrollmentResponseData(self.course, data, demo.GENDER)

    def test_recent_activity(self):
        self.assertRecentActivityResponseData(self.course, at.ANY)
        self.assertRecentActivityResponseData(self.course, at.ATTEMPTED_PROBLEM)
        self.assertRecentActivityResponseData(self.course, at.PLAYED_VIDEO)
        self.assertRecentActivityResponseData(self.course, at.POSTED_FORUM)
