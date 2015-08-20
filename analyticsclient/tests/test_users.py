import json

import httpretty

from analyticsclient.exceptions import NotFoundError
from analyticsclient.tests import ClientTestCase


class UserTests(ClientTestCase):
    def setUp(self):
        super(UserTests, self).setUp()
        self.username = "TestUser"
        httpretty.enable()

    def tearDown(self):
        super(UserTests, self).tearDown()
        httpretty.disable()

    def test_not_found(self):
        """ User API calls should raise a NotFoundError when provided with an invalid user ID. """

        username = "B@dName!"
        uri = self.get_api_url('users/{0}/'.format(username))
        httpretty.register_uri(httpretty.GET, uri, status=404)

        user = self.client.users(username)
        with self.assertRaises(NotFoundError):
            user.profile()

    def test_profile(self):

        body = {
            "id": 123,
            "username": self.username,
            "last_login": "2015-05-28T00:08:45Z",
            "date_joined": "2015-05-28T00:08:43Z",
            "is_staff": False,
            "email": "test@example.com",
            "name": "Test User",
            "gender": "unknown",
            "year_of_birth": 1903,
            "level_of_education": "unknown"
        }

        uri = self.get_api_url('users/{0}/'.format(self.username))
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.client.users(self.username).profile())
