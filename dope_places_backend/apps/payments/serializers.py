# apps/payments/serializers.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework import serializers


# Local imports
from .models import Payment


# Create your serializers here.
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
