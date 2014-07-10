

class Course(object):

    """
    Course-related analytics.
    """

    def __init__(self, client, course_id):
        """
        Initialize the Course client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.
            course_id (str): String identifying the course (e.g. edX/DemoX/Demo_Course)

        """
        self.client = client
        self.course_id = course_id

    @property
    def recent_active_user_count(self):
        """A count of users who have recently interacted with the course in any way."""
        # TODO: should we return something more structured than a python dict?
        return self.client.get('courses/{0}/recent_activity'.format(self.course_id))

    @property
    def recent_problem_activity_count(self):
        """A count of users who have recently attempted a problem."""
        # TODO: Can we avoid passing around strings like "ATTEMPTED_PROBLEM" in the data pipeline and the client?
        return self.client.get(
            'courses/{0}/recent_activity?activity_type=ATTEMPTED_PROBLEM'.format(self.course_id))

    def enrollment(self, demographic=None):
        uri = 'courses/{0}/enrollment'.format(self.course_id)
        if demographic:
            uri += '/%s' % demographic
        return self.client.get(uri)
