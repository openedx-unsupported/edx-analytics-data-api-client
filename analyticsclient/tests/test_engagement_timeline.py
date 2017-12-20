import json

import httpretty

from analyticsclient.exceptions import NotFoundError
from analyticsclient.tests import ClientTestCase


class EngagementTimelineTests(ClientTestCase):

    def setUp(self):
        super(EngagementTimelineTests, self).setUp()
        self.username = 'edx'
        self.course_id = 'edX/DemoX/Demo_Course'
        self.engagement_timeline = self.client.engagement_timeline(self.username, self.course_id)
        httpretty.enable()

    def tearDown(self):
        super(EngagementTimelineTests, self).tearDown()
        httpretty.disable()

    def test_not_found(self):
        not_a_valid_course_id = 'foobar'
        uri = self.get_api_url('engagement_timelines/{username}/?course_id={course_id}'
                               .format(username=self.username, course_id=not_a_valid_course_id))
        httpretty.register_uri(httpretty.GET, uri, status=404)

        engagement_timeline = self.client.engagement_timeline(self.username, not_a_valid_course_id)
        self.assertRaises(NotFoundError, engagement_timeline.get)

    def test_engagement_timeline(self):
        body = {
            "days": [
                {
                    "date": "date",
                    "problems_attempted": 0,
                    "problems_completed": 0,
                    "discussion_contributions": 0,
                    "videos_viewed": 3
                }
            ]
        }
        uri = self.get_api_url('engagement_timelines/{username}/?course_id={course_id}'
                               .format(username=self.username, course_id=self.course_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.engagement_timeline.get())
