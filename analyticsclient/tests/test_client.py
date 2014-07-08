import json

import httpretty

from analyticsclient.client import Client
from analyticsclient.exceptions import ClientError
from analyticsclient.tests import ClientTestCase


class ClientTests(ClientTestCase):
    def setUp(self):
        super(ClientTests, self).setUp()
        httpretty.enable()
        self.test_endpoint = 'test'
        self.test_uri = self.get_api_url(self.test_endpoint)

    def tearDown(self):
        httpretty.disable()

    def test_has_resource(self):
        httpretty.register_uri(httpretty.GET, self.test_uri, body='')
        self.assertEquals(self.client.has_resource(self.test_endpoint), True)

    def test_missing_resource(self):
        httpretty.register_uri(httpretty.GET, self.test_uri, body='', status=404)
        self.assertEquals(self.client.has_resource(self.test_endpoint), False)

    def test_failed_authentication(self):
        client = Client(base_url=self.api_url, auth_token='atoken')
        httpretty.register_uri(httpretty.GET, self.test_uri, body='', status=401)

        self.assertEquals(client.has_resource(self.test_endpoint), False)
        self.assertEquals(httpretty.last_request().headers['Authorization'], 'Token atoken')

    def test_get(self):
        data = {'foo': 'bar'}
        httpretty.register_uri(httpretty.GET, self.test_uri, body=json.dumps(data))
        self.assertEquals(self.client.get(self.test_endpoint), data)

        # Bad JSON
        httpretty.register_uri(httpretty.GET, self.test_uri, body=json.dumps(data)[:6])
        with self.assertRaises(ClientError):
            self.client.get(self.test_endpoint)
