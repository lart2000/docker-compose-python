# apps/customers/serializers.py
# Python imports


# Django imports
from django.contrib.auth import get_user_model


# Third party apps imports
from rest_framework import serializers


# Local imports
from apps.core.fields import UserField, CustomImageField
from .models import Admin


# Create your serializers here.
class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user = UserField(read_only=True)
    username = serializers.EmailField(write_only=True)
    avatar = CustomImageField(required=False)

    class Meta:
        model = Admin
        fields = ('id', 'user', 'username', 'password', 'avatar', 'superadmin')

    def create(self, validated_data):
        user_data = {
            'password': validated_data.pop('password'),
            'username': validated_data.pop('username'),
            'first_name': self.initial_data['first_name'],
            'last_name' : self.initial_data['last_name']
        }
        if hasattr(self.context['request'].auth.user, 'admin'):
            admin = Admin.objects.get(user=self.context['request'].auth.user)
            if admin.superadmin:
                user = get_user_model().objects.create_user(**user_data)
                return Admin.objects.create(user=user, **validated_data)
            else:
                msg = "Needs to be a super administrator"
                raise serializers.ValidationError({'Message': msg}, code="Unauthorized")
        else:
            msg = "Needs to be a super administrator"
            raise serializers.ValidationError({'Message': msg}, code="Unauthorized")

    def update(self, instance, validated_data):
        if hasattr(self.context['request'].auth.user, 'admin'):
            admin = Admin.objects.get(user=self.context['request'].auth.user)
            if admin.superadmin:
                if 'first_name' in self.initial_data:
                    instance.user.first_name = self.initial_data.pop('first_name')
                if 'last_name' in self.initial_data:
                    instance.user.last_name = self.initial_data.pop('last_name')
                if 'email' in self.initial_data:
                    instance.user.email = self.initial_data.pop('email')
                if 'avatar' in self.initial_data:
                    instance.avatar = self.initial_data.pop('avatar')
                instance.user.save()
                instance.save()
                return instance
            else:
                msg = "Needs to be a super administrator"
                raise serializers.ValidationError({'Message': msg}, code="Unauthorized")
        else:
            msg = "Needs to be a super administrator"
            raise serializers.ValidationError({'Message': msg}, code="Unauthorized")
