# pylint: disable=arguments-differ
import ddt

from analyticsclient.tests import ClientTestCase, APIListTestCase


@ddt.ddt
class CourseSummariesTests(APIListTestCase, ClientTestCase):

    endpoint = 'course_summaries'
    id_field = 'course_ids'
    uses_post_method = True

    @ddt.data(
        ['123'],
        ['123', '456']
    )
    def test_programs(self, programs):
        """Course summaries can be called with programs."""
        self.kwarg_test(programs=programs)

    @ddt.data(
        (['edx/demo/course'], ['course_id'], ['enrollment_modes'], ['123']),
        (['edx/demo/course', 'another/demo/course'], ['course_id', 'enrollment_modes'],
         ['created', 'pacing_type'], ['123', '456'])
    )
    @ddt.unpack
    def test_all_parameters(self, course_ids, fields, exclude, programs):
        """Course summaries can be called with all parameters including programs."""
        self.kwarg_test(course_ids=course_ids, fields=fields, exclude=exclude, programs=programs)
