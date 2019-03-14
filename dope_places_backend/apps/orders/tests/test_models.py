# apps/orders/tests/test_models.py
# Python imports


# Django imports
from django.test import TestCase


# Third party apps imports
from model_mommy import mommy


# Local imports
from apps.countries.models import Country
from apps.customers.models import Customer
from apps.items.models import Item
from apps.proxies.models import Proxy
from ..models import Order


# Create your model tests here.
class OrderTestCase(TestCase):
    def setUp(self):
        self.order = mommy.make(Order, _fill_optional=True)
        self.field_list = [field.name for field in Order._meta.get_fields()]

    def test_have_fields_needed_by_he_business(self):
        self.assertTrue('country' in self.field_list)
        self.assertTrue('customer' in self.field_list)
        self.assertTrue('name' in self.field_list)
        self.assertTrue('notes' in self.field_list)
        self.assertTrue('proxy' in self.field_list)

    def test_have_country_relation(self):
        self.assertTrue(self.order.country.__class__ is Country)

    def test_have_customer_relation(self):
        self.assertTrue(self.order.customer.__class__ is Customer)

    def test_have_items_relation(self):
        self.assertTrue(self.order.items.model is Item)

    def test_have_proxy_relation(self):
        self.assertTrue(self.order.proxy.__class__ is Proxy)

    def test_method_str(self):
        self.assertIn(self.order.customer.user.username, self.order.__str__())

    def tearDown(self):
        self.order.delete()
