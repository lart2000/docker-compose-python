# apps/customers/tests/test_models.py
# Python imports


# Django imports
from django.contrib.auth import get_user_model
from django.test import TestCase


# Third party apps imports
from model_mommy import mommy


# Local imports
from apps.countries.models import Country
from ..models import Customer


# Create your model tests here.
class CustomerTestCase(TestCase):
    def setUp(self):
        self.customer = mommy.make(Customer, _fill_optional=True)
        self.field_list = [field.name for field in Customer._meta.get_fields()]

    def test_have_fields_needed_by_he_business(self):
        self.assertTrue('avatar' in self.field_list)
        self.assertTrue('country' in self.field_list)
        self.assertTrue('paypal_email' in self.field_list)
        self.assertTrue('user' in self.field_list)

    def test_have_country_relation(self):
        self.assertTrue(self.customer.country.__class__ is Country)

    def test_have_user_relation(self):
        self.assertTrue(self.customer.user.__class__ is get_user_model())

    def test_method_str(self):
        self.assertIn(self.customer.user.username, self.customer.__str__())

    def tearDown(self):
        self.customer.delete()
