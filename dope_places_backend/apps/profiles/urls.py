# apps/profiles/urls.py
# Python imports


# Django imports


# from django.contrib.auth import views as auth_views
from django.conf.urls import url


# Third party apps imports


# Local imports
from .views import ProfileAPIView, exchange_token
from apps.payments.viewsets import setup_transaction


# Register your urls here.
urlpatterns = [
    url(r'profile/', ProfileAPIView.as_view(), name='profile-list'),
    url(r'social/(?P<backend>[^/]+)/$', exchange_token),
    url(r'paypal/(?P<id>[0-9]+)/$', setup_transaction),
]

