# apps/customers/tests/test_viewsets.py
# Python imports


# Django imports
from django.urls import reverse


# Third party apps imports
from model_mommy import mommy
from model_mommy.random_gen import gen_email, gen_image_field, gen_string
from rest_framework import status
from rest_framework.test import APITestCase


# Local imports
from apps.countries.models import Country
from ..models import Customer


# Create your viewset tests here.
class CustomerAPITestCase(APITestCase):
    def setUp(self):
        self.countries = mommy.make(Country, _fill_optional=True, _quantity=10)
        self.country_random = Country.objects.order_by('?').last()
        self.customers = mommy.make(
            Customer, _fill_optional=True, _quantity=10)
        self.customer_random = Customer.objects.order_by('?').last()
        self.customers_list_url = reverse('api_v1:customer-list')
        self.customer_detail_url = reverse(
            'api_v1:customer-detail', kwargs={'pk': self.customer_random.pk})

    def test_list(self):
        self.client.force_authenticate(self.customer_random.user)
        response = self.client.get(self.customers_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_create(self):
        data = {
            'avatar': gen_image_field(),
            'country': self.country_random.id,
            'first_name': gen_string(max_length=10),
            'last_name': gen_string(max_length=10),
            'password': gen_string(max_length=10),
            'paypal_email': gen_email(),
            'username': gen_email()
        }
        response = self.client.post(self.customers_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        self.client.force_authenticate(self.customer_random.user)
        response = self.client.get(self.customer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('avatar' in response.data)
        self.assertTrue('country' in response.data)
        self.assertTrue('paypal_email' in response.data)
        self.assertTrue('user' in response.data)

    def test_partial_update(self):
        self.client.force_authenticate(self.customer_random.user)
        paypal_email = gen_email()
        first_name = gen_string(max_length=20)
        last_name = gen_string(max_length=20)
        data = {
            'country': self.country_random.id,
            'paypal_email': paypal_email,
            'first_name': first_name,
            'last_name': last_name
        }
        response = self.client.patch(self.customer_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['country'], self.country_random.id)
        self.assertEqual(response.data['paypal_email'], paypal_email)
        self.assertEqual(response.data['user']['first_name'], first_name)
        self.assertEqual(response.data['user']['last_name'], last_name)

    def tearDown(self):
        for country in Country.objects.all():
            country.delete()
        for customer in Customer.objects.all():
            customer.delete()
