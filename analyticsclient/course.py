import warnings
from urllib.parse import urlencode

from analyticsclient.base import PostableCourseIDsEndpoint
from analyticsclient.constants import activity_types, data_formats
from analyticsclient.exceptions import InvalidRequestError


class Course(PostableCourseIDsEndpoint):
    """Course-related analytics."""

    def __init__(self, client, course_id):
        """
        Initialize the Course client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.
            course_id (str): String identifying the course (e.g. edX/DemoX/Demo_Course)

        """
        super().__init__(client)
        self.course_id = str(course_id)

    def enrollment(self, demographic=None, start_date=None, end_date=None, data_format=data_formats.JSON):
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
        path = f'courses/{self.course_id}/enrollment/'
        if demographic:
            path += f'{demographic}/'

        params = {}
        if start_date:
            params['start_date'] = start_date

        if end_date:
            params['end_date'] = end_date

        querystring = urlencode(params)
        if querystring:
            path += f'?{querystring}'

        return self.client.get(path, data_format=data_format)

    def activity(self, activity_type=activity_types.ANY, start_date=None, end_date=None, data_format=data_formats.JSON):
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

        path = f'courses/{self.course_id}/activity/'
        querystring = urlencode(params)
        path += f'?{querystring}'

        return self.client.get(path, data_format=data_format)

    def recent_activity(self, activity_type=activity_types.ANY, data_format=data_formats.JSON):
        """
        Get the recent course activity.

        Arguments:
            activity_type (str): The type of recent activity to return. Defaults to ANY.
            data_format (str): Format in which data should be returned
        """
        warnings.warn('recent_activity has been deprecated! Use activity instead.', DeprecationWarning)

        path = f'courses/{self.course_id}/recent_activity/?activity_type={activity_type}'
        return self.client.get(path, data_format=data_format)

    def problems(self, data_format=data_formats.JSON):
        """
        Get the problems for the course.

        Arguments:
            data_format (str): Format in which data should be returned
        """
        path = f'courses/{self.course_id}/problems/'
        return self.client.get(path, data_format=data_format)

    def problems_and_tags(self, data_format=data_formats.JSON):
        """
        Get the problems for the course with assigned tags.

        Arguments:
            data_format (str): Format in which data should be returned
        """
        path = f'courses/{self.course_id}/problems_and_tags/'
        return self.client.get(path, data_format=data_format)

    def reports(self, report_name, data_format=data_formats.JSON):
        """
        Get CSV download information for a particular report in the course.

        Arguments:
            report_name (str): Report name, e.g. "problem_response"
        """
        path = f'courses/{self.course_id}/reports/{report_name}/'
        return self.client.get(path, data_format=data_format)

    def videos(self, data_format=data_formats.JSON):
        """
        Get the videos for the course.

        Arguments:
            data_format (str): Format in which data should be returned
        """
        path = f'courses/{self.course_id}/videos/'
        return self.client.get(path, data_format=data_format)
