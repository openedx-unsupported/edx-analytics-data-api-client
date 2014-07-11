from unittest import TestCase
from analyticsclient import activity_type, demographic


class HelperTests(TestCase):
    """
    Basic checks for typos.
    """

    def test_activity_type(self):
        self.assertEqual('any', activity_type.ANY)
        self.assertEqual('attempted_problem', activity_type.ATTEMPTED_PROBLEM)
        self.assertEqual('played_video', activity_type.PLAYED_VIDEO)
        self.assertEqual('posted_forum', activity_type.POSTED_FORUM)

    def test_demographic(self):
        self.assertEqual('birth_year', demographic.BIRTH_YEAR)
        self.assertEqual('education', demographic.EDUCATION)
        self.assertEqual('gender', demographic.GENDER)
