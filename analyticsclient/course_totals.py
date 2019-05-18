from __future__ import absolute_import

from analyticsclient.base import PostableCourseIDsEndpoint
from analyticsclient.constants import data_formats


class CourseTotals(PostableCourseIDsEndpoint):
    """Course aggregate data."""

    path = 'course_totals/'

    def course_totals(self, course_ids=None, data_format=data_formats.JSON):
        """
        Get aggregate data about courses.

        For more detailed parameter and return type descriptions, see the
        edX Analytics Data API documentation.

        Arguments:
            course_ids (list[str]): Course IDs to filter by.
            data_format (str): Data format for response.
                               Must be data_format.JSON or data_format.CSV.
        """
        return self.do_request(course_ids=course_ids, data={}, data_format=data_format)
