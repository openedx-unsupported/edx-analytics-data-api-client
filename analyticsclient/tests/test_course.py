import json
import re

import httpretty

from analyticsclient.constants import activity_type as at
from analyticsclient.constants import data_format
from analyticsclient.constants import demographic as demo
from analyticsclient.exceptions import NotFoundError, InvalidRequestError
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

    def assertCorrectEnrollmentUrl(self, course, demographic=None):
        """ Verifies that the enrollment URL is correct. """

        uri = self.get_api_url('courses/{0}/enrollment/'.format(course.course_id))
        if demographic:
            uri += '%s/' % demographic

        httpretty.register_uri(httpretty.GET, uri, body='{}')
        course.enrollment(demographic)

        date = '2014-01-01'
        httpretty.reset()
        httpretty.register_uri(httpretty.GET, '{0}?start_date={1}'.format(uri, date), body='{}')
        course.enrollment(demographic, start_date=date)

        httpretty.reset()
        httpretty.register_uri(httpretty.GET, '{0}?end_date={1}'.format(uri, date), body='{}')
        course.enrollment(demographic, end_date=date)

        httpretty.reset()
        httpretty.register_uri(httpretty.GET, '{0}?start_date={1}&end_date={1}'.format(uri, date), body='{}')
        course.enrollment(demographic, start_date=date, end_date=date)

    def assertCorrectActivityUrl(self, course, activity_type=None):
        """ Verifies that the activity URL is correct. """

        uri = self.get_api_url('courses/{0}/activity/'.format(course.course_id))
        if activity_type:
            uri += '?activity_type=%s' % activity_type

        httpretty.register_uri(httpretty.GET, uri, body='{}')
        course.activity(activity_type)

        date = '2014-01-01'
        httpretty.reset()
        httpretty.register_uri(httpretty.GET, '{0}&start_date={1}'.format(uri, date), body='{}')
        course.activity(activity_type, start_date=date)

        httpretty.reset()
        httpretty.register_uri(httpretty.GET, '{0}&end_date={1}'.format(uri, date), body='{}')
        course.activity(activity_type, end_date=date)

        httpretty.reset()
        httpretty.register_uri(httpretty.GET, '{0}&start_date={1}&end_date={1}'.format(uri, date), body='{}')
        course.activity(activity_type, start_date=date, end_date=date)

    @httpretty.activate
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

    def test_recent_activity(self):
        self.assertRecentActivityResponseData(self.course, at.ANY)
        self.assertRecentActivityResponseData(self.course, at.ATTEMPTED_PROBLEM)
        self.assertRecentActivityResponseData(self.course, at.PLAYED_VIDEO)
        self.assertRecentActivityResponseData(self.course, at.POSTED_FORUM)

    def test_not_found(self):
        """ Course calls should raise a NotFoundError when provided with an invalid course. """

        course_id = 'not-a-course-id'
        uri = self.get_api_url('courses/{0}/'.format(course_id))
        uri = re.compile(r'^' + re.escape(uri) + r'.*$')
        httpretty.register_uri(httpretty.GET, uri, status=404)

        course = self.client.courses(course_id)
        self.assertRaises(NotFoundError, course.recent_activity, at.ANY)
        self.assertRaises(NotFoundError, course.enrollment, demo.EDUCATION)

    def test_invalid_parameter(self):
        """ Course calls should raise a InvalidRequestError when parameters are invalid. """

        uri = self.get_api_url('courses/{0}/'.format(self.course_id))
        uri = re.compile(r'^' + re.escape(uri) + r'.*$')
        httpretty.register_uri(httpretty.GET, uri, status=400)

        self.assertRaises(InvalidRequestError, self.course.recent_activity, 'not-a-an-activity-type')
        self.assertRaises(InvalidRequestError, self.course.enrollment, 'not-a-demographic')

    def test_enrollment(self):
        self.assertCorrectEnrollmentUrl(self.course, None)
        self.assertCorrectEnrollmentUrl(self.course, demo.BIRTH_YEAR)
        self.assertCorrectEnrollmentUrl(self.course, demo.EDUCATION)
        self.assertCorrectEnrollmentUrl(self.course, demo.GENDER)
        self.assertCorrectEnrollmentUrl(self.course, demo.LOCATION)

    def test_activity(self):
        self.assertRaises(InvalidRequestError, self.assertCorrectActivityUrl, self.course, None)
        self.assertCorrectActivityUrl(self.course, at.ANY)
        self.assertCorrectActivityUrl(self.course, at.ATTEMPTED_PROBLEM)
        self.assertCorrectActivityUrl(self.course, at.PLAYED_VIDEO)
        self.assertCorrectActivityUrl(self.course, at.POSTED_FORUM)

    def test_enrollment_data_format(self):
        uri = self.get_api_url('courses/{0}/enrollment/'.format(self.course.course_id))

        httpretty.register_uri(httpretty.GET, uri, body='{}')

        self.course.enrollment()
        self.assertEquals(httpretty.last_request().headers['Accept'], 'application/json')

        httpretty.register_uri(httpretty.GET, uri, body='not-json')
        self.course.enrollment(data_format=data_format.CSV)
        self.assertEquals(httpretty.last_request().headers['Accept'], 'text/csv')

    @httpretty.activate
    def test_problems(self):

        body = [
            {
                'module_id': 'i4x://a/b/c'
            }
        ]

        uri = self.get_api_url('courses/{0}/problems/'.format(self.course_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.course.problems())

    def test_user_list(self):
        body = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "username": "honor",
                    "last_login": "2015-06-29T19:50:00Z",
                    "date_joined": "2014-11-19T04:06:46Z",
                    "is_staff": False,
                    "email": "honor@example.com",
                    "name": "honor",
                    "gender": "unknown",
                    "year_of_birth": None,
                    "level_of_education": "unknown"
                }
            ]
        }

        uri = self.get_api_url('courses/{0}/users/'.format(self.course_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.course.list_users())

    def test_user_list_pagination(self):
        uri = self.get_api_url('courses/{0}/users/?'.format(self.course_id))
        uri = re.compile(r'^' + re.escape(uri) + r'.*$')
        httpretty.register_uri(httpretty.GET, uri, body="{}")

        self.course.list_users()
        self.assertIsNotNone(httpretty.last_request())
        self.assertEqual(httpretty.last_request().querystring, {"limit": ['100'], "page": ['1']})

        self.course.list_users(page=30, limit=10)
        self.assertEqual(httpretty.last_request().querystring, {"limit": ['10'], "page": ['30']})

    @httpretty.activate
    def test_videos(self):

        body = [
            {
                'pipeline_video_id': '0fac49ba',
                'encoded_module_id': 'i4x-a-b-c',
                'duration': 600,
                'segment_length': 5,
                'start_views': 50,
                'end_views': 1,
                'created': '2015-01-01T00:01:00'
            }
        ]

        uri = self.get_api_url('courses/{0}/videos/'.format(self.course_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.course.videos())
