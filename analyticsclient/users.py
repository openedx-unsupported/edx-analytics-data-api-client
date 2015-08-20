import analyticsclient.constants.data_format as DF


class User(object):
    """ User-related analytics. """

    def __init__(self, client, username):
        """
        Initialize the API client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.
            username (string): The username to query

        """
        self.client = client
        self.username = username

    def profile(self, data_format=DF.JSON):
        """
        Get the user's basic information.

        Arguments:
            data_format (str): Format in which data should be returned
        """
        path = 'users/{0}/'.format(self.username)
        return self.client.get(path, data_format=data_format)
