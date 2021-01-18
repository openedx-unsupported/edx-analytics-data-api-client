from urllib.parse import urlencode

from analyticsclient.base import PostableCourseIDsEndpoint
from analyticsclient.constants import data_formats


class EngagementTimeline(PostableCourseIDsEndpoint):
    """Engagement Timeline."""

    def __init__(self, client, username, course_id):
        """
        Initialize the EngagementTimeline client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.
            username (str): String identifying the user (e.g. jbradley)
            course_id (str): String identifying the course (e.g. edX/DemoX/Demo_Course)

        """
        super().__init__(client)

        self.username = str(username)
        self.course_id = str(course_id)

    def get(self):
        """Get a particular learner's engagement timeline for a particular course."""
        querystring = urlencode({'course_id': self.course_id})
        path = f'engagement_timelines/{self.username}/?{querystring}'
        return self.client.get(path, data_format=data_formats.JSON)
