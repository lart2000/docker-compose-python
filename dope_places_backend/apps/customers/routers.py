# apps/customers/routers.py
# Python imports


# Django imports


# Third party apps imports


# Local imports
from .viewsets import CustomerViewSet, CustomerSocialUserViewSet


# Create your routers here.
customers = (
    (r'customer', CustomerViewSet),
    (r'socialcustomer', CustomerSocialUserViewSet),
)
