from unittest import TestCase
from analyticsclient.constants import activity_type, demographic, education_level, gender, enrollment_modes


class HelperTests(TestCase):
    """
    Basic checks for typos.
    """

    def test_activity_types(self):
        self.assertEqual('any', activity_type.ANY)
        self.assertEqual('attempted_problem', activity_type.ATTEMPTED_PROBLEM)
        self.assertEqual('played_video', activity_type.PLAYED_VIDEO)
        self.assertEqual('posted_forum', activity_type.POSTED_FORUM)

    def test_demographics(self):
        self.assertEqual('birth_year', demographic.BIRTH_YEAR)
        self.assertEqual('education', demographic.EDUCATION)
        self.assertEqual('gender', demographic.GENDER)

    def test_education_levels(self):
        self.assertEqual('none', education_level.NONE)
        self.assertEqual('other', education_level.OTHER)
        self.assertEqual('primary', education_level.PRIMARY)
        self.assertEqual('junior_secondary', education_level.JUNIOR_SECONDARY)
        self.assertEqual('secondary', education_level.SECONDARY)
        self.assertEqual('associates', education_level.ASSOCIATES)
        self.assertEqual('bachelors', education_level.BACHELORS)
        self.assertEqual('masters', education_level.MASTERS)
        self.assertEqual('doctorate', education_level.DOCTORATE)
        self.assertEqual('unknown', education_level.UNKNOWN)

    def test_genders(self):
        self.assertEqual('female', gender.FEMALE)
        self.assertEqual('male', gender.MALE)
        self.assertEqual('other', gender.OTHER)
        self.assertEqual('unknown', gender.UNKNOWN)

    def test_enrollment_modes(self):
        self.assertEqual('audit', enrollment_modes.AUDIT)
        self.assertEqual('honor', enrollment_modes.HONOR)
        self.assertEqual('professional', enrollment_modes.PROFESSIONAL)
        self.assertEqual('verified', enrollment_modes.VERIFIED)
