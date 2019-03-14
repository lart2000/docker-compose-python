# apps/customers/models.py
# Python imports


# Django imports
from django.db import models
from django.conf import settings

# Third party apps imports


# Local imports
from apps.core.models import BaseProfile


# Create your models here.
class Customer(BaseProfile):

    def __str__(self):
        return self.user.username


class PasswordToken(models.Model):
    token_password = models.CharField(max_length=1024, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)

    def __str__(self):
        return self.user.username
