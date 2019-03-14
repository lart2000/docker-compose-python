# apps/countries/fields.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework.serializers import PrimaryKeyRelatedField


# Local imports
from .models import Country
from .serializers import CountrySerializer


# Create your serializers here.
class CountryField(PrimaryKeyRelatedField):
    queryset = Country.objects.all()

    def to_representation(self, value):
        serializer = CountrySerializer(Country.objects.get(pk=value.pk))
        return serializer.data
