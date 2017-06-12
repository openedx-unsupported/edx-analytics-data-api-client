from unittest import TestCase

import ddt
import httpretty

from analyticsclient.client import Client


class ClientTestCase(TestCase):
    """Base class for client-related tests."""

    def setUp(self):
        """Configure Client."""
        self.api_url = 'http://localhost:9999/api/v0'
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
class APIListTestCase(object):
    """Base class for API list view tests."""

    # Override in the subclass:
    endpoint = 'list'
    id_field = 'id'
    uses_post_method = False

    def setUp(self):
        """Set up the test case."""
        super(APIListTestCase, self).setUp()
        self.base_uri = self.get_api_url('{}/'.format(self.endpoint))
        self.client_class = getattr(self.client, self.endpoint)()
        httpretty.enable()

    def verify_last_querystring_equal(self, expected_query):
        """Convenience method for asserting the last request was made with the expected query parameters."""
        self.assertDictEqual(httpretty.last_request().querystring, expected_query)

    def expected_query(self, **kwargs):
        """Pack the query arguments into expected format for http pretty."""
        query = {}
        for field, data in kwargs.items():
            if data is not None:
                query[field] = [','.join(data)]
        return query

    @httpretty.activate
    def kwarg_test(self, **kwargs):
        """Construct URL with given query parameters and check if it is what we expect."""
        httpretty.reset()
        if self.uses_post_method:
            httpretty.register_uri(httpretty.POST, self.base_uri, body='{}')
            getattr(self.client_class, self.endpoint)(**kwargs)
            self.assertDictEqual(httpretty.last_request().parsed_body or {}, kwargs)
        else:
            uri_template = '{uri}?'
            for key in kwargs:
                uri_template += '%s={%s}' % (key, key)
            uri = uri_template.format(uri=self.base_uri, **kwargs)
            httpretty.register_uri(httpretty.GET, uri, body='{}')
            getattr(self.client_class, self.endpoint)(**kwargs)
            self.verify_last_querystring_equal(self.expected_query(**kwargs))

    def test_all_items_url(self):
        """Endpoint can be called without parameters."""
        httpretty.register_uri(
            httpretty.POST if self.uses_post_method else httpretty.GET,
            self.base_uri, body='{}'
        )
        getattr(self.client_class, self.endpoint)()

    @ddt.data(
        ['edx/demo/course'],
        ['edx/demo/course', 'another/demo/course']
    )
    def test_courses_ids(self, ids):
        """Endpoint can be called with IDs."""
        self.kwarg_test(**{self.id_field: ids})

    @ddt.data(
        ['course_id'],
        ['course_id', 'enrollment_modes']
    )
    def test_fields(self, fields):
        """Endpoint can be called with fields."""
        self.kwarg_test(fields=fields)

    @ddt.data(
        ['course_id'],
        ['course_id', 'enrollment_modes']
    )
    def test_exclude(self, exclude):
        """Endpoint can be called with exclude."""
        self.kwarg_test(exclude=exclude)

    @ddt.data(
        (['edx/demo/course'], ['course_id'], ['enrollment_modes']),
        (['edx/demo/course', 'another/demo/course'], ['course_id', 'enrollment_modes'],
         ['created', 'pacing_type'])
    )
    @ddt.unpack
    def test_all_parameters(self, ids, fields, exclude):
        """Endpoint can be called with all parameters."""
        self.kwarg_test(**{self.id_field: ids, 'fields': fields, 'exclude': exclude})
