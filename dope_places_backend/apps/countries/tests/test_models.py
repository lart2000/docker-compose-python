# apps/countries/tests/test_models.py
# Python imports


# Django imports
from django.test import TestCase


# Third party apps imports
from model_mommy import mommy


# Local imports
from ..models import Country


# Create your model tests here.
class CountryTestCase(TestCase):
    def setUp(self):
        self.country = mommy.make(Country, _fill_optional=True)
        self.field_list = [field.name for field in Country._meta.get_fields()]

    def test_have_fields_needed_by_he_business(self):
        self.assertTrue('currency' in self.field_list)
        self.assertTrue('name' in self.field_list)

    def test_method_str(self):
        self.assertIn(self.country.name, self.country.__str__())

    def tearDown(self):
        self.country.delete()
