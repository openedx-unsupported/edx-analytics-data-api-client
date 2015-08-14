import json
import re

import httpretty

from analyticsclient.exceptions import NotFoundError
from analyticsclient.tests import ClientTestCase


class UserTests(ClientTestCase):
    def setUp(self):
        super(UserTests, self).setUp()
        self.user_id = 10000
        httpretty.enable()

    def tearDown(self):
        super(UserTests, self).tearDown()
        httpretty.disable()

    def test_not_found(self):
        """ User API calls should raise a NotFoundError when provided with an invalid user ID. """

        user_id = 555
        uri = self.get_api_url('users/{0}/'.format(user_id))
        httpretty.register_uri(httpretty.GET, uri, status=404)

        user = self.client.users(user_id)
        with self.assertRaises(NotFoundError):
            user.profile()

    def test_profile(self):

        body = {
            "id": self.user_id,
            "username": "TestUser",
            "last_login": "2015-05-28T00:08:45Z",
            "date_joined": "2015-05-28T00:08:43Z",
            "is_staff": False,
            "email": "test@example.com",
            "name": "Test User",
            "gender": "unknown",
            "year_of_birth": 1903,
            "level_of_education": "unknown"
        }

        uri = self.get_api_url('users/{0}/'.format(self.user_id))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.client.users(self.user_id).profile())
