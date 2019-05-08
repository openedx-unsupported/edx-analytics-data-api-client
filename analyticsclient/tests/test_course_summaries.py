from __future__ import absolute_import
import datetime
import ddt

from analyticsclient.tests import (
    APIListTestCase,
    APIWithPostableIDsTestCase,
    ClientTestCase
)


@ddt.ddt
class CourseSummariesTests(APIListTestCase, APIWithPostableIDsTestCase, ClientTestCase):

    endpoint = 'course_summaries'
    id_field = 'course_ids'

    _LIST_PARAMS = frozenset([
        'course_ids',
        'availability',
        'pacing_type',
        'program_ids',
        'fields',
        'exclude',
    ])
    _STRING_PARAMS = frozenset([
        'text_search',
        'order_by',
        'sort_order',
    ])
    _INT_PARAMS = frozenset([
        'page',
        'page_size',
    ])
    _ALL_PARAMS = _LIST_PARAMS | _STRING_PARAMS | _INT_PARAMS
    other_params = _ALL_PARAMS

    # Test URL encoding (note: '+' is not handled right by httpretty, but it works in practice)
    _TEST_STRING = 'Aa1_-:/* '

    @ddt.data(
        (_LIST_PARAMS, ['a', 'b', 'c']),
        (_LIST_PARAMS, [_TEST_STRING]),
        (_LIST_PARAMS, []),
        (_STRING_PARAMS, _TEST_STRING),
        (_STRING_PARAMS, ''),
        (_INT_PARAMS, 1),
        (_INT_PARAMS, 0),
        (frozenset(), None),
    )
    @ddt.unpack
    def test_most_parameters(self, param_names, param_value):
        """Course summaries can be called with all parameters."""
        params = {param_name: None for param_name in self._ALL_PARAMS}
        params.update({param_name: param_value for param_name in param_names})
        self.verify_query_params(**params)

    @ddt.data(
        ('2018-11-22', '2018-11-22'),
        (datetime.date(2018, 11, 22), '2018-11-22'),
    )
    @ddt.unpack
    def test_recent_date(self, recent, recent_str):
        """recent_date can be passed as a date object or string."""
        params = {'recent_date': recent}
        expected = self.expected_query(**{'recent_date': recent_str})
        self.verify_query_params_vs_expected(params, expected)
