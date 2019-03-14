# apps/admins/models.py
# Python imports


# Django imports
from django.db import models
from django.conf import settings

# Third party apps imports


# Local imports


# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    superadmin = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Admins'

    def __str__(self):
        return self.user.username
