import json

import httpretty
import mock
import requests.exceptions
from testfixtures import log_capture

from analyticsclient.constants import data_format
from analyticsclient.client import Client
from analyticsclient.exceptions import ClientError, TimeoutError
from analyticsclient.tests import ClientTestCase


class ClientTests(ClientTestCase):
    def setUp(self):
        super(ClientTests, self).setUp()
        httpretty.enable()
        self.test_endpoint = 'test'
        self.test_url = self.get_api_url(self.test_endpoint)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_date_format(self):
        self.assertEqual(Client.DATE_FORMAT, '%Y-%m-%d')
        self.assertEqual(Client('').DATE_FORMAT, '%Y-%m-%d')

    def test_has_resource(self):
        httpretty.register_uri(httpretty.GET, self.test_url, body='')
        self.assertEquals(self.client.has_resource(self.test_endpoint), True)

    def test_missing_resource(self):
        httpretty.register_uri(httpretty.GET, self.test_url, body='', status=404)
        self.assertEquals(self.client.has_resource(self.test_endpoint), False)

    def test_failed_authentication(self):
        client = Client(base_url=self.api_url, auth_token='atoken')
        httpretty.register_uri(httpretty.GET, self.test_url, body='', status=401)

        self.assertEquals(client.has_resource(self.test_endpoint), False)
        self.assertEquals(httpretty.last_request().headers['Authorization'], 'Token atoken')

    def test_get(self):
        data = {'foo': 'bar'}
        httpretty.register_uri(httpretty.GET, self.test_url, body=json.dumps(data))
        self.assertEquals(self.client.get(self.test_endpoint), data)

    def test_post(self):
        data = {'foo': 'bar'}
        httpretty.register_uri(httpretty.POST, self.test_url, body=json.dumps(data))
        self.assertEquals(self.client.post(self.test_endpoint), data)

    def test_get_invalid_response_body(self):
        """ Verify that client raises a ClientError if the response body cannot be properly parsed. """

        data = {'foo': 'bar'}
        httpretty.register_uri(httpretty.GET, self.test_url, body=json.dumps(data)[:6])
        with self.assertRaises(ClientError):
            self.client.get(self.test_endpoint)

    def test_strip_trailing_slash(self):
        url = 'http://example.com'
        client = Client(url)
        self.assertEqual(client.base_url, url)

        url_with_slash = 'http://example.com/'
        client = Client(url_with_slash)
        self.assertEqual(client.base_url, url)

    # pylint: disable=protected-access
    @mock.patch('requests.get', side_effect=requests.exceptions.Timeout)
    @log_capture()
    def test_request_timeout(self, mock_get, lc):
        url = self.test_url
        timeout = None
        headers = {'Accept': 'application/json'}

        self.assertRaises(
            TimeoutError,
            self.client._request,
            self.client.METHOD_GET,
            self.test_endpoint,
            timeout=timeout
        )
        msg = 'Response from {0} exceeded timeout of {1}s.'.format(self.test_endpoint, self.client.timeout)
        lc.check(('analyticsclient.client', 'ERROR', msg))
        lc.clear()
        mock_get.assert_called_once_with(url, headers=headers, timeout=self.client.timeout)
        mock_get.reset_mock()

        timeout = 10
        self.assertRaises(
            TimeoutError,
            self.client._request,
            self.client.METHOD_GET,
            self.test_endpoint,
            timeout=timeout
        )
        mock_get.assert_called_once_with(url, headers=headers, timeout=timeout)
        msg = 'Response from {0} exceeded timeout of {1}s.'.format(self.test_endpoint, timeout)
        lc.check(('analyticsclient.client', 'ERROR', msg))

    def test_request_format(self):
        httpretty.register_uri(httpretty.GET, self.test_url, body='{}')

        response = self.client.get(self.test_endpoint)
        self.assertEquals(httpretty.last_request().headers['Accept'], 'application/json')
        self.assertDictEqual(response, {})

        httpretty.register_uri(httpretty.GET, self.test_url, body='not-json')
        response = self.client.get(self.test_endpoint, data_format=data_format.CSV)
        self.assertEquals(httpretty.last_request().headers['Accept'], 'text/csv')
        self.assertEqual(response, 'not-json')

        httpretty.register_uri(httpretty.GET, self.test_url, body='{}')
        response = self.client.get(self.test_endpoint, data_format=data_format.JSON)
        self.assertEquals(httpretty.last_request().headers['Accept'], 'application/json')
        self.assertDictEqual(response, {})

    def test_unsupported_method(self):
        self.assertRaises(
            ValueError,
            self.client._request,
            'PATCH',
            self.test_endpoint
        )
