# apps/customers/fields.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework.serializers import PrimaryKeyRelatedField


# Local imports
from .models import Customer
from .serializers import CustomerSerializer


# Create your serializers here.
class CustomerField(PrimaryKeyRelatedField):
    queryset = Customer.objects.all()

    def to_representation(self, value):
        instance = self.get_queryset().get(pk=value.pk)
        serializer = CustomerSerializer(instance)
        return serializer.data
