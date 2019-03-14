# apps/core/serializers.py
# Python imports


# Django imports
from django.contrib.auth import get_user_model


# Third party apps imports
from rest_framework import serializers


# Local imports


# Create your serializers here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
