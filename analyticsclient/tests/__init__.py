from unittest import TestCase

import ddt
import httpretty

from analyticsclient.client import Client


class ClientTestCase(TestCase):
    """Base class for client-related tests."""

    def setUp(self):
        """Configure Client."""
        self.api_url = 'http://localhost:9999/api/v1'
        self.client = Client(self.api_url)

    def get_api_url(self, path):
        """
        Build an API URL with the specified path.

        Arguments:
            path (str): Path to be appended to the URL

        Returns:
            Complete API URL and path
        """
        return "{0}/{1}".format(self.client.base_url, path)


@ddt.ddt
class APIWithIDsTestCase(object):
    """Base class for tests for API endpoints that take lists of IDs."""

    # Override in the subclass:
    endpoint = 'endpoint'
    id_field = 'id'
    other_params = frozenset()

    def setUp(self):
        """Set up the test case."""
        super(APIWithIDsTestCase, self).setUp()
        self.base_uri = self.get_api_url('{}/'.format(self.endpoint))
        self.client_class = getattr(self.client, self.endpoint)()
        httpretty.enable()

    def verify_last_querystring_equal(self, expected_query):
        """Convenience method for asserting the last request was made with the expected query parameters."""
        self.assertDictEqual(httpretty.last_request().querystring, expected_query)

    def expected_query(self, **kwargs):
        """Pack the query arguments into expected format for http pretty."""
        return {
            field: (
                [','.join(data)] if isinstance(data, list) else [str(data)]
            )
            for field, data in kwargs.iteritems()
            if data
        }

    @httpretty.activate
    def verify_query_params(self, **kwargs):
        """Construct URL with given query parameters and check if it is what we expect."""
        httpretty.reset()

        uri_template = '{uri}?'
        for key in kwargs:
            uri_template += '%s={%s}' % (key, key)
        uri = uri_template.format(uri=self.base_uri, **kwargs)

        httpretty.register_uri(httpretty.GET, uri, body='{}')
        getattr(self.client_class, self.endpoint)(**kwargs)
        self.verify_last_querystring_equal(self.expected_query(**kwargs))

    def fill_in_empty_params_with_dummies(self, **kwargs):
        """Fill in non-provided parameters with dummy values so they are tested."""
        params = {param: '.' for param in self.other_params}
        params.update(kwargs)
        return params

    @ddt.data(
        [],
        ['edx/demo/course'],
        ['edx/demo/course', 'another/demo/course'],
    )
    def test_url_with_params(self, ids):
        """Endpoint can be called with parameters, including IDs."""
        params = self.fill_in_empty_params_with_dummies(**{self.id_field: ids})
        self.verify_query_params(**params)

    def test_url_without_params(self):
        """Endpoint can be called without parameters."""
        httpretty.register_uri(httpretty.GET, self.base_uri, body='{}')
        getattr(self.client_class, self.endpoint)()


class APIWithPostableIDsTestCase(APIWithIDsTestCase):
    """Base class for tests for API endpoints that can POST a list of course IDs."""

    @httpretty.activate
    def verify_post_data(self, **kwargs):
        """Construct POST request with parameters and check if it is what we expect."""
        httpretty.reset()
        httpretty.register_uri(httpretty.POST, self.base_uri, body='{}')
        getattr(self.client_class, self.endpoint)(**kwargs)

        expected_body = kwargs.copy()
        for key, val in expected_body.iteritems():
            if not isinstance(val, list):
                expected_body[key] = [val]
        actual_body = httpretty.last_request().parsed_body
        self.assertDictEqual(actual_body or {}, expected_body)

    def test_request_with_many_ids(self):
        """Endpoint can be called with a large number of ID parameters."""
        params = self.fill_in_empty_params_with_dummies(**{self.id_field: ['id'] * 10000})
        self.verify_post_data(**params)


@ddt.ddt
class APIListTestCase(APIWithIDsTestCase):
    """Base class for API list view tests."""

    @ddt.data(
        ['course_id'],
        ['course_id', 'enrollment_modes']
    )
    def test_fields(self, fields):
        """Endpoint can be called with fields."""
        self.verify_query_params(fields=fields)

    @ddt.data(
        ['course_id'],
        ['course_id', 'enrollment_modes']
    )
    def test_exclude(self, exclude):
        """Endpoint can be called with exclude."""
        self.verify_query_params(exclude=exclude)

    @ddt.data(
        (['edx/demo/course'], ['course_id'], ['enrollment_modes']),
        (['edx/demo/course', 'another/demo/course'], ['course_id', 'enrollment_modes'],
         ['created', 'pacing_type'])
    )
    @ddt.unpack
    def test_all_list_parameters(self, ids, fields, exclude):
        """Endpoint can be called with IDs, fields, and exlude parameters."""
        params = self.fill_in_empty_params_with_dummies(
            **{self.id_field: ids, 'fields': fields, 'exclude': exclude}
        )
        self.verify_query_params(**params)
