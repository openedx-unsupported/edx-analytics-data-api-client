from __future__ import absolute_import

import datetime

from analyticsclient.base import PostableCourseIDsEndpoint
from analyticsclient.constants import data_formats


class CourseSummaries(PostableCourseIDsEndpoint):
    """Course summaries."""

    path = 'course_summaries/'

    def course_summaries(
            self,
            course_ids=None,
            availability=None,
            pacing_type=None,
            program_ids=None,
            text_search=None,
            recent_date=None,
            order_by=None,
            sort_order=None,
            page=None,
            page_size=None,
            request_all=False,
            fields=None,
            exclude=None,
            data_format=data_formats.JSON,
    ):
        """
        Get list of summaries.

        For more detailed parameter and return type descriptions, see the
        edX Analytics Data API documentation.

        Arguments:
            course_ids (list[str]): Course IDs to filter by.
            availability (list[str]) Availabilities to filter by.
            pacing_type (list[str]): Pacing types to filter by.
            program_ids (list[str]): Course IDs of programs to filter by.
            text_search (str): Sub-string to search for in course titles and IDs.
            recent_date (date): A date in the past to compute enrollement count
                                change relative to; can be a python date or
                                'YYYY-MM-DD' string
            order_by (str): Summary field to sort by.
            sort_order (str): Order of the sort.
            page (int): Page number.
            page_size (int): Size of page.
            request_all (bool): Whether all summaries should be returned, or just a
                                single page. Overrides `page` and `page_size`.
            fields (list[str]) Fields of course summaries to return in response.
            exclude (list[str]) Fields of course summaries to NOT return in response.
            data_format (str): Data format for response. Must be data_format.JSON or
                               data_format.CSV.

        Returns: dict
        """
        raw_data = {
            'availability': availability,
            'pacing_type': pacing_type,
            'program_ids': program_ids,
            'text_search': text_search,
            'recent_date': recent_date,
            'order_by': order_by,
            'sort_order': sort_order,
            'page': page,
            'page_size': page_size,
            'fields': fields,
            'exclude': exclude,
            'all': request_all,
        }
        data = {
            key: value
            for key, value in raw_data.items()
            if value
        }
        if recent_date and isinstance(recent_date, datetime.date):
            data['recent_date'] = recent_date.strftime('%Y-%m-%d')

        return self.do_request(course_ids=course_ids, data=data, data_format=data_format)
