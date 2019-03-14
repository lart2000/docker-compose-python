# apps/core/fields.py
# Python imports


# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model


# Third party apps imports
from rest_framework.serializers import ImageField, PrimaryKeyRelatedField


# Local imports
from .serializers import UserSerializer


# Create your serializers here.
class UserField(PrimaryKeyRelatedField):

    def to_representation(self, value):
        user = get_user_model().objects.get(pk=value.pk)
        serializer = UserSerializer(user)
        return serializer.data


class CustomImageField(ImageField):
    def to_representation(self, value):
        try:
            return settings.API_HOSTNAME + value.url
        except Exception:
            return None
