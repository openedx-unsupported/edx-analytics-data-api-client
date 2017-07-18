from unittest import TestCase
from analyticsclient.constants import activity_types, demographics, education_levels, genders, enrollment_modes


class HelperTests(TestCase):
    """
    Basic checks for typos.
    """

    def test_activity_types(self):
        self.assertEqual('any', activity_types.ANY)
        self.assertEqual('attempted_problem', activity_types.ATTEMPTED_PROBLEM)
        self.assertEqual('played_video', activity_types.PLAYED_VIDEO)
        self.assertEqual('posted_forum', activity_types.POSTED_FORUM)

    def test_demographics(self):
        self.assertEqual('birth_year', demographics.BIRTH_YEAR)
        self.assertEqual('education', demographics.EDUCATION)
        self.assertEqual('gender', demographics.GENDER)

    def test_education_levels(self):
        self.assertEqual('none', education_levels.NONE)
        self.assertEqual('other', education_levels.OTHER)
        self.assertEqual('primary', education_levels.PRIMARY)
        self.assertEqual('junior_secondary', education_levels.JUNIOR_SECONDARY)
        self.assertEqual('secondary', education_levels.SECONDARY)
        self.assertEqual('associates', education_levels.ASSOCIATES)
        self.assertEqual('bachelors', education_levels.BACHELORS)
        self.assertEqual('masters', education_levels.MASTERS)
        self.assertEqual('doctorate', education_levels.DOCTORATE)

    def test_genders(self):
        self.assertEqual('female', genders.FEMALE)
        self.assertEqual('male', genders.MALE)
        self.assertEqual('other', genders.OTHER)
        self.assertEqual('unknown', genders.UNKNOWN)

    def test_enrollment_modes(self):
        self.assertEqual('audit', enrollment_modes.AUDIT)
        self.assertEqual('credit', enrollment_modes.CREDIT)
        self.assertEqual('honor', enrollment_modes.HONOR)
        self.assertEqual('professional', enrollment_modes.PROFESSIONAL)
        self.assertEqual('verified', enrollment_modes.VERIFIED)
