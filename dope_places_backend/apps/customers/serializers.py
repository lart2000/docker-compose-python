# apps/customers/serializers.py
# Python imports


# Django imports
from django.contrib.auth import get_user_model


# Third party apps imports
from rest_framework import serializers


# Local imports
from apps.core.fields import UserField, CustomImageField
from .models import Customer


# Create your serializers here.
class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    user = UserField(read_only=True)
    username = serializers.EmailField(write_only=True)
    avatar = CustomImageField(required=False)

    class Meta:
        model = Customer
        fields = (
            'id', 'avatar', 'country', 'first_name', 'last_name', 'password',
            'paypal_email', 'user', 'username',)

    def create(self, validated_data):
        user_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
            'username': validated_data.pop('username'),
        }
        user = get_user_model().objects.create_user(**user_data)
        return Customer.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        if 'first_name' in validated_data:
            instance.user.first_name = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            instance.user.last_name = validated_data.pop('last_name')
        instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
