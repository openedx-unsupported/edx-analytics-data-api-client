import ddt

from analyticsclient.tests import APIListTestCase, ClientTestCase


@ddt.ddt
class ProgramsTests(APIListTestCase, ClientTestCase):

    endpoint = 'programs'
    id_field = 'program_ids'
