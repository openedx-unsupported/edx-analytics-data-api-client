import json

import httpretty

from analyticsclient.tests import ClientTestCase


class StatusTests(ClientTestCase):
    @httpretty.activate
    def test_alive(self):
        """
        Alive status should be True if server responds with HTTP 200, otherwise False.
        """

        # Normal behavior
        httpretty.register_uri(httpretty.GET, self.get_api_url('status'))
        self.assertTrue(self.client.status.alive)

        # "Kill" the server (assuming there is nothing running at API_URL)
        httpretty.reset()
        self.assertFalse(self.client.status.alive)

    @httpretty.activate
    def test_authenticated(self):
        """
        Authenticated status should be True if client is authenticated, otherwise False.
        """

        # Normal behavior
        httpretty.register_uri(httpretty.GET, self.get_api_url('authenticated'))
        self.assertTrue(self.client.status.authenticated)

        # Non-authenticated user
        httpretty.register_uri(httpretty.GET, self.get_api_url('authenticated'), status=401)
        self.assertFalse(self.client.status.authenticated)

    @httpretty.activate
    def test_healthy(self):
        """
        Healthy status should be True if server is alive and can respond to requests, otherwise False.
        """

        # Unresponsive server
        self.assertFalse(self.client.status.healthy)

        body = {
            'overall_status': 'OK',
            'detailed_status': {
                'database_connection': 'OK'
            }
        }

        # Normal behavior
        httpretty.register_uri(httpretty.GET, self.get_api_url('health'), body=json.dumps(body))
        self.assertTrue(self.client.status.healthy)

        # Sick server
        body['overall_status'] = 'BAD'
        httpretty.register_uri(httpretty.GET, self.get_api_url('health'), body=json.dumps(body))
        self.assertFalse(self.client.status.healthy)

        # Odd response
        del body['overall_status']
        httpretty.register_uri(httpretty.GET, self.get_api_url('health'), body=json.dumps(body))
        self.assertFalse(self.client.status.healthy)
