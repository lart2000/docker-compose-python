# apps/profiles/serializers.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework import serializers


# Local imports
from apps.customers.fields import CustomerField
from apps.proxies.fields import ProxyField


# Create your serializers here.
class ProfileSerializer(serializers.Serializer):
    customer = CustomerField()
    proxy = ProxyField()
    role = serializers.SerializerMethodField()

    def get_role(self, user):
        try:
            if user.customer:
                return 'customer'
        except Exception:
            pass
        try:
            if user.proxy:
                return 'proxy'
        except Exception:
            pass
        return 'Not profile asigned'
