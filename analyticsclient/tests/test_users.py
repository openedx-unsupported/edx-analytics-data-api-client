import json
import re

import httpretty

from analyticsclient.exceptions import NotFoundError
from analyticsclient.tests import ClientTestCase


class UserListTests(ClientTestCase):
    def setUp(self):
        super(UserListTests, self).setUp()
        httpretty.enable()

    def tearDown(self):
        super(UserListTests, self).tearDown()
        httpretty.disable()

    def test_list(self):
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

        uri = self.get_api_url('users/')
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps(body))
        self.assertEqual(body, self.client.user_list().list_users())

    def test_pagination(self):
        uri = self.get_api_url('users/?')
        uri = re.compile(r'^' + re.escape(uri) + r'.*$')
        httpretty.register_uri(httpretty.GET, uri, body="{}")

        self.client.user_list().list_users()
        self.assertIsNotNone(httpretty.last_request())
        self.assertEqual(httpretty.last_request().querystring, {"limit": ['100'], "page": ['1']})

        self.client.user_list().list_users(page=30, limit=10)
        self.assertEqual(httpretty.last_request().querystring, {"limit": ['10'], "page": ['30']})


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
