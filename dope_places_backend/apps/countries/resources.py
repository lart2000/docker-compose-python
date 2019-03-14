# apps/countries/resources.py
# Python imports


# Django imports


# Third party apps imports
from import_export.resources import ModelResource


# Local imports
from .models import Country


# Create your resources here.
class CountryResource(ModelResource):
    class Meta:
        model = Country
