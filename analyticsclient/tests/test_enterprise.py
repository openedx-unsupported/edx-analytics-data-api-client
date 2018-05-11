"""
Tests for the Enterprise Data API client.
"""

import json
import uuid

import httpretty

from analyticsclient.tests import ClientTestCase


class EnterpriseTests(ClientTestCase):

    def setUp(self):
        super(EnterpriseTests, self).setUp()
        self.enterprise_customer_uuid = uuid.uuid4()
        self.enterprise = self.client.enterprise(self.enterprise_customer_uuid)
        httpretty.enable()

    def tearDown(self):
        super(EnterpriseTests, self).tearDown()
        httpretty.disable()

    def test_enterprise_enrollment(self):
        body = [
            {
                "model": "enterprise_data.EnterpriseEnrollment",
                "pk": 1,
                "fields": {
                    "enterprise_id": "ee5e6b3a-069a-4947-bb8d-d2dbc323396c",
                    "enterprise_name": "Enterprise 1",
                    "lms_user_id": 11,
                    "enterprise_user_id": 1,
                    "course_id": "edX/Open_DemoX/edx_demo_course",
                    "enrollment_created_timestamp": "2014-06-27 16:02:38",
                    "user_current_enrollment_mode": "verified",
                    "consent_granted": 0,
                    "letter_grade": "Pass",
                    "has_passed": 1,
                    "passed_timestamp": "2017-05-09 16:27:34.690065",
                    "enterprise_sso_user_id": "harry",
                    "course_title": "All about acceptance testing!",
                    "course_start": "2016-09-01",
                    "course_end": "2016-12-01",
                    "course_pacing_type": "instructor_paced",
                    "course_duration_weeks": "8",
                    "course_min_effort": 2,
                    "course_max_effort": 4,
                    "user_account_creation_date": "2015-02-12 23:14:35",
                    "user_email": "test@example.com",
                    "user_username": "test_user"
                }
            },
        ]
        uri = self.get_api_url('enterprise/{}/enrollments/'.format(self.enterprise_customer_uuid))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.enterprise.enrollments())
