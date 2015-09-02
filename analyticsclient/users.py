import analyticsclient.constants.data_format as DF


class UserProblemWeeklyData(object):
    """ Get user problem history per week. """

    def __init__(self, client, course_id, user_id):
        """
        Initialize the API client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.
            user_id (int): The ID of the user

        """
        self.client = client
        self.course_id = course_id
        self.user_id = user_id

    def weekly_problem_data(self, data_format=DF.JSON):
        """
        Get weekly reports about problem history of a user.

        Arguments:
            data_format (str): Format in which data should be returned
        """
        path = 'courses/{}/users/{}/problem_data/'.format(self.course_id, self.user_id)
        return self.client.get(path, data_format=data_format)
