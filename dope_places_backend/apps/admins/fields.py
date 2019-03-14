# apps/admins/fields.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework.serializers import PrimaryKeyRelatedField


# Local imports
from .models import Admin
from .serializers import AdminSerializer


# Create your fields here.
class AdminField(PrimaryKeyRelatedField):
    #queryset = Admin.objects.all()

    def to_representation(self, value):
        instance = self.get_queryset().get(pk=value.pk)
        serializer = AdminSerializer(instance)
        return serializer.data
