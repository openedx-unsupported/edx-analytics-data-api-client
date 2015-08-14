import analyticsclient.constants.data_format as DF


class User(object):
    """ User-related analytics. """

    def __init__(self, client, user_id):
        """
        Initialize the API client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.
            user_id (int): The ID of the user

        """
        self.client = client
        self.user_id = unicode(user_id)

    def profile(self, data_format=DF.JSON):
        """
        Get the user's basic information.

        Arguments:
            data_format (str): Format in which data should be returned
        """
        path = 'users/{0}/'.format(self.user_id)
        return self.client.get(path, data_format=data_format)
