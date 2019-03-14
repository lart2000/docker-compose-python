# apps/orders/tests/test_viewsets.py
# Python imports


# Django imports
from django.urls import reverse
from django.utils.http import urlencode


# Third party apps imports
from model_mommy import mommy
from model_mommy.random_gen import gen_decimal, gen_string, gen_text, gen_url
from rest_framework import status
from rest_framework.test import APITestCase


# Local imports
from apps.countries.models import Country
from apps.customers.models import Customer
from apps.items.models import Item
from ..models import Order


# Create your viewset tests here.
class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.country = mommy.make(Country, _fill_optional=True)
        self.customer = mommy.make(Customer, _fill_optional=True)
        self.customer_other = mommy.make(Customer, _fill_optional=True)
        self.orders = mommy.make(
            Order, status=Order.DRAFT, customer=self.customer,
            _fill_optional=True, _quantity=10)
        self.order_random = Order.objects.order_by('?').last()
        self.items = mommy.make(
            Item, order=self.order_random, _fill_optional=True, _quantity=5)
        self.item_random = Item.objects.order_by('?').last()
        self.orders_list_url = reverse('api_v1:order-list')
        self.order_detail_url = reverse(
            'api_v1:order-detail', kwargs={'pk': self.order_random.pk})

    def test_list_customer(self):
        self.client.force_authenticate(self.order_random.customer.user)
        response = self.client.get(self.orders_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_list_proxy(self):
        self.client.force_authenticate(self.order_random.proxy.user)
        response = self.client.get(self.orders_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_by_status(self):
        self.client.force_authenticate(self.order_random.customer.user)
        orders_list_by_status = '{0}?{1}'.format(
            self.orders_list_url, urlencode({'status': Order.DELIVERY}))
        response = self.client.get(orders_list_by_status)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_by_status_other_customer(self):
        self.client.force_authenticate(self.customer_other.user)
        orders_list_by_status = '{0}?{1}'.format(
            self.orders_list_url, urlencode({'status': Order.DRAFT}))
        response = self.client.get(orders_list_by_status)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create(self):
        self.client.force_authenticate(self.order_random.customer.user)
        data = {
            'name': gen_string(50),
            'country': self.country.id,
            'items': [
                {
                    'link': gen_url(),
                    'name': gen_string(10),
                    'notes': gen_text(),
                    'price': gen_decimal(7, 2)
                }, {
                    'link': gen_url(),
                    'name': gen_string(10),
                    'notes': gen_text(),
                    'price': gen_decimal(7, 2)
                }, {
                    'link': gen_url(),
                    'name': gen_string(10),
                    'notes': gen_text(),
                    'price': gen_decimal(7, 2)
                }, {
                    'link': gen_url(),
                    'name': gen_string(10),
                    'notes': gen_text(),
                    'price': gen_decimal(7, 2)
                }, {
                    'link': gen_url(),
                    'name': gen_string(10),
                    'notes': gen_text(),
                    'price': gen_decimal(7, 2)
                },
            ],
        }
        response = self.client.post(self.orders_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['items']), len(data['items']))

    def test_retrieve(self):
        self.client.force_authenticate(self.order_random.customer.user)
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('country' in response.data)
        self.assertTrue('customer' in response.data)
        self.assertTrue('items' in response.data)
        self.assertTrue('notes' in response.data)
        self.assertTrue('proxy' in response.data)
        self.assertTrue('status' in response.data)

    def test_partial_update_assign_proxy(self):
        self.client.force_authenticate(self.order_random.proxy.user)
        self.order_random.proxy = None
        self.order_random.status = Order.POSTED
        self.order_random.save()
        response = self.client.patch(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['proxy'] is not None)
        self.assertEqual(response.data['status'], Order.MATCHED)

    def test_partial_update_from_customer_no_data(self):
        self.client.force_authenticate(self.order_random.customer.user)
        self.order_random.proxy = None
        self.order_random.save()
        response = self.client.patch(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['proxy'] is None)

    def test_partial_update_from_customer(self):
        self.client.force_authenticate(self.order_random.customer.user)
        self.order_random.proxy = None
        self.order_random.status = Order.DRAFT
        self.order_random.save()
        data = {
            'name': gen_string(50),
            'items': [
                {
                    'link': gen_url(),
                    'name': gen_string(10),
                    'notes': gen_text(),
                    'order': None,
                    'price': gen_decimal(7, 2)
                }, {
                    'link': gen_url(),
                    'name': gen_string(10),
                    'notes': gen_text(),
                    'order': None,
                    'price': gen_decimal(7, 2)
                }, {
                    'link': self.item_random.link,
                    'name': self.item_random.name,
                    'notes': self.item_random.notes,
                    'order': self.item_random.order.id,
                    'price': self.item_random.price
                }
            ]
        }
        response = self.client.patch(
            self.order_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['proxy'] is None)
        self.assertEqual(len(response.data['items']), 3)
        self.assertEqual(Item.objects.filter(
            order=self.item_random.order).count(), 3)

    def tearDown(self):
        for country in Country.objects.all():
            country.delete()
        for customer in Customer.objects.all():
            customer.delete()
        for order in Order.objects.all():
            order.delete()
        for item in Item.objects.all():
            item.delete()
