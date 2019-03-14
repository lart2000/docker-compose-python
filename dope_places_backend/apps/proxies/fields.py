# apps/customers/fields.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework.serializers import PrimaryKeyRelatedField


# Local imports
from .models import Proxy
from .serializers import ProxySerializer


# Create your serializers here.
class ProxyField(PrimaryKeyRelatedField):
    queryset = Proxy.objects.all()

    def to_representation(self, value):
        instance = self.get_queryset().get(pk=value.pk)
        serializer = ProxySerializer(instance)
        return serializer.data
