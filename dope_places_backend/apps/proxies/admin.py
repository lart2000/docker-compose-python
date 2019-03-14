# apps/proxies/admin.py
# Python imports


# Django imports
from django.contrib import admin


# Third party apps imports


# Local imports
from .models import Proxy


# Register your models here.
@admin.register(Proxy)
class ProxyModelAdmin(admin.ModelAdmin):
    pass
