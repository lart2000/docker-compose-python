# apps/countries/tests/test_viewsets.py
# Python imports


# Django imports
from django.urls import reverse


# Third party apps imports
from model_mommy import mommy
from model_mommy.random_gen import gen_string
from rest_framework import status
from rest_framework.test import APITestCase


# Local imports
from apps.customers.models import Customer
from ..models import Country


# Create your viewset tests here.
class CountryAPITestCase(APITestCase):
    def setUp(self):
        self.countries = mommy.make(Country, _fill_optional=True, _quantity=10)
        self.countries_list_url = reverse('api_v1:country-list')
        self.country_random = Country.objects.order_by('?').last()
        self.customer = mommy.make(
            Customer, country=self.country_random, _fill_optional=True)
        self.country_detail_url = reverse(
            'api_v1:country-detail', kwargs={'pk': self.country_random.pk})

    def test_list(self):
        response = self.client.get(self.countries_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_create(self):
        self.client.force_authenticate(self.customer.user)
        data = {
            'currency': gen_string(max_length=50),
            'name': gen_string(max_length=50)
        }
        response = self.client.post(self.countries_list_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve(self):
        self.client.force_authenticate(self.customer.user)
        response = self.client.get(self.country_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('currency' in response.data)
        self.assertTrue('name' in response.data)

    def test_partial_update(self):
        self.client.force_authenticate(self.customer.user)
        data = {
            'currency': gen_string(max_length=50),
            'name': gen_string(max_length=50)
        }
        response = self.client.patch(self.country_detail_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        self.client.force_authenticate(self.customer.user)
        data = {
            'currency': gen_string(max_length=50),
            'name': gen_string(max_length=50)
        }
        response = self.client.put(self.country_detail_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_destroy(self):
        self.client.force_authenticate(self.customer.user)
        response = self.client.delete(self.country_detail_url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def tearDown(self):
        for country in Country.objects.all():
            country.delete()
        for customer in Customer.objects.all():
            customer.delete()
