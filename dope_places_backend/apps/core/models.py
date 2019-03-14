# apps/core/models.py
# Python imports


# Django imports
from django.conf import settings
from django.db import models


# Third party apps imports


# Local imports


# Create your models here.
class BaseProfile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    country = models.ForeignKey('countries.Country', models.CASCADE)
    paypal_email = models.EmailField(max_length=254)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)

    class Meta:
        abstract = True
