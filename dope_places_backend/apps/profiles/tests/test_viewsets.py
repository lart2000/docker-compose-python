# apps/profiles/tests/test_viewsets.py
# Python imports


# Django imports
from django.contrib.auth import get_user_model
from django.urls import reverse


# Third party apps imports
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase


# Local imports
from apps.customers.models import Customer
from apps.proxies.models import Proxy


# Create your viewset tests here.
class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.customer = mommy.make(Customer, _fill_optional=True)
        self.proxy = mommy.make(Proxy, _fill_optional=True)
        self.user = mommy.make(get_user_model(), _fill_optional=True)
        self.profile_list_url = reverse('profile_urls:profile-list')

    def test_list_customer(self):
        self.client.force_authenticate(self.customer.user)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('avatar' in response.data['customer'])
        self.assertTrue('country' in response.data['customer'])
        self.assertTrue('email' in response.data['customer']['user'])
        self.assertTrue('first_name' in response.data['customer']['user'])
        self.assertTrue('last_name' in response.data['customer']['user'])
        self.assertTrue('paypal_email' in response.data['customer'])
        self.assertTrue('role' in response.data)

    def test_list_proxy(self):
        self.client.force_authenticate(self.proxy.user)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('avatar' in response.data['proxy'])
        self.assertTrue('country' in response.data['proxy'])
        self.assertTrue('email' in response.data['proxy']['user'])
        self.assertTrue('first_name' in response.data['proxy']['user'])
        self.assertTrue('last_name' in response.data['proxy']['user'])
        self.assertTrue('paypal_email' in response.data['proxy'])
        self.assertTrue('role' in response.data)

    def test_list_not_authenticated(self):
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('detail' in response.data)

    def test_list_not_customer_not_proxy(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        for customer in Customer.objects.all():
            customer.delete()
        for proxy in Proxy.objects.all():
            proxy.delete()
