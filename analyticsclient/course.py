import urllib
import analyticsclient.activity_type as at


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

    def enrollment(self, demographic=None, start_date=None, end_date=None):
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
            end_date (str): Maxmimum date for returned enrollment data
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

        return self.client.get(path)

    def recent_activity(self, activity_type=at.ANY):
        """
        Get the recent course activity.

        Arguments:
            activity_type (str): The type of recent activity to return. Defaults to ANY.
        """
        return self.client.get('courses/{0}/recent_activity/?activity_type={1}'.format(self.course_id, activity_type))
