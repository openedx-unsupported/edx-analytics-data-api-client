

from analyticsclient.tests import APIWithPostableIDsTestCase, ClientTestCase


class CourseTotalsTests(APIWithPostableIDsTestCase, ClientTestCase):

    endpoint = 'course_totals'
    id_field = 'course_ids'
    other_params = frozenset()
