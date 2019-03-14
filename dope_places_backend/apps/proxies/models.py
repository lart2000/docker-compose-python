# apps/proxies/models.py
# Python imports


# Django imports


# Third party apps imports


# Local imports
from apps.core.models import BaseProfile


# Create your models here.
class Proxy(BaseProfile):

    class Meta:
        verbose_name_plural = 'Proxies'

    def __str__(self):
        return self.user.username
