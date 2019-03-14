# apps/items/tests/test_models.py
# Python imports


# Django imports
from django.test import TestCase


# Third party apps imports
from model_mommy import mommy


# Local imports
from ..models import Item


# Create your model tests here.
class ItemTestCase(TestCase):
    def setUp(self):
        self.item = mommy.make(Item, _fill_optional=True)
        self.field_list = [field.name for field in Item._meta.get_fields()]

    def test_have_fields_needed_by_he_business(self):
        self.assertTrue('name' in self.field_list)

    def test_method_str(self):
        self.assertIn(self.item.name, self.item.__str__())

    def tearDown(self):
        self.item.delete()
