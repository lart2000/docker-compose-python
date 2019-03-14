# apps/countries/serializers.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework import serializers


# Local imports
from .models import Country


# Create your serializers here.
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'currency', 'name')
