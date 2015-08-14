import urllib
import warnings
import analyticsclient.constants.activity_type as AT
import analyticsclient.constants.data_format as DF
from analyticsclient.exceptions import InvalidRequestError


class Course(object):
    """ Course-related analytics. """

    def __init__(self, client, course_id):
        """
        Initialize the Course client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.
            course_id (str): String identifying the course (e.g. edX/DemoX/Demo_Course)

        """
        self.client = client
        self.course_id = unicode(course_id)

    def enrollment(self, demographic=None, start_date=None, end_date=None, data_format=DF.JSON):
        """
        Get course enrollment data.

        Specify a start or end date to retrieve all data for the date range. If no start or end date is specifying, data
          for the most-recent date will be returned. All dates are in the UTC timezone and should be formatted as
          YYYY-mm-dd (e.g. 2014-01-31).

        Specify a demographic to retrieve data grouped by the specified demographic. If no demographic is specified,
          data will be across all demographics.

        Arguments:
            demographic (str): Demographic by which enrollment data should be grouped.
            start_date (str): Minimum date for returned enrollment data
            end_date (str): Maximum date for returned enrollment data
            data_format (str): Format in which data should be returned
        """
        path = 'courses/{0}/enrollment/'.format(self.course_id)
        if demographic:
            path += '{0}/'.format(demographic)

        params = {}
        if start_date:
            params['start_date'] = start_date

        if end_date:
            params['end_date'] = end_date

        querystring = urllib.urlencode(params)
        if querystring:
            path += '?{0}'.format(querystring)

        return self.client.get(path, data_format=data_format)

    def activity(self, activity_type=AT.ANY, start_date=None, end_date=None, data_format=DF.JSON):
        """
        Get the course student activity.

        Arguments:
            activity_type (str): The type of recent activity to return. Defaults to ANY.
            data_format (str): Format in which data should be returned
        """
        if not activity_type:
            raise InvalidRequestError('activity_type cannot be None.')

        params = {
            'activity_type': activity_type
        }

        if start_date:
            params['start_date'] = start_date

        if end_date:
            params['end_date'] = end_date

        path = 'courses/{0}/activity/'.format(self.course_id)
        querystring = urllib.urlencode(params)
        path += '?{0}'.format(querystring)

        return self.client.get(path, data_format=data_format)

    def recent_activity(self, activity_type=AT.ANY, data_format=DF.JSON):
        """
        Get the recent course activity.

        Arguments:
            activity_type (str): The type of recent activity to return. Defaults to ANY.
            data_format (str): Format in which data should be returned
        """
        warnings.warn('recent_activity has been deprecated! Use activity instead.', DeprecationWarning)

        path = 'courses/{0}/recent_activity/?activity_type={1}'.format(self.course_id, activity_type)
        return self.client.get(path, data_format=data_format)

    def problems(self, data_format=DF.JSON):
        """
        Get the problems for the course.

        Arguments:
            data_format (str): Format in which data should be returned
        """
        path = 'courses/{0}/problems/'.format(self.course_id)
        return self.client.get(path, data_format=data_format)

    def list_users(self, page=1, limit=100, data_format=DF.JSON):
        """
        Get the list of users.

        Arguments:
            page (int): Which page of results to return
            limit (int): The maximum number of users to include on each page
            data_format (str): Format in which data should be returned
        """
        path = 'courses/{}/users/?page={}&limit={}'.format(self.course_id, page, limit)
        return self.client.get(path, data_format=data_format)

    def videos(self, data_format=DF.JSON):
        """
        Get the videos for the course.

        Arguments:
            data_format (str): Format in which data should be returned
        """
        path = 'courses/{0}/videos/'.format(self.course_id)
        return self.client.get(path, data_format=data_format)
