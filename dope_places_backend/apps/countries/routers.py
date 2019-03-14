# apps/countries/routers.py
# Python imports


# Django imports


# Third party apps imports


# Local imports
from .viewsets import CountryViewSet


# Create your routers here.
countries = (
    (r'country', CountryViewSet),
)
