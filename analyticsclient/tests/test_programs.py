import ddt

from analyticsclient.tests import ClientTestCase, APIListTestCase


@ddt.ddt
class ProgramsTests(APIListTestCase, ClientTestCase):

    endpoint = 'programs'
    id_field = 'program_ids'
