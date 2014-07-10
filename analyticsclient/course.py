import analyticsclient.activity_type as at


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
        self.course_id = unicode(course_id)

    def enrollment(self, demographic):
        """
        Get course enrollment data grouped by demographic.

        Arguments:
            demographic (str): Demographic by which enrollment data should be grouped.
        """
        return self.client.get('courses/{0}/enrollment/{1}'.format(self.course_id, demographic))

    def recent_activity(self, activity_type=at.ANY):
        """
        Get the recent course activity.

        Arguments:
            activity_type (str): The type of recent activity to return. Defaults to ANY.
        """
        return self.client.get('courses/{0}/recent_activity?activity_type={1}'.format(self.course_id, activity_type))
