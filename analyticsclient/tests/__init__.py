from unittest import TestCase

from analyticsclient.client import Client


class ClientTestCase(TestCase):
    """ Base class for client-related tests. """

    def setUp(self):
        """ Configure Client. """
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
