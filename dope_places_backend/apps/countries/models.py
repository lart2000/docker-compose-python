# apps/countries/models.py
# Python imports


# Django imports
from django.db import models


# Third party apps imports


# Local imports


# Create your models here.
class Country(models.Model):
    code = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name
