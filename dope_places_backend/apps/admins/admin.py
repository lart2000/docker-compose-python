# apps/customers/admin.py
# Python imports


# Django imports
from django.contrib import admin


# Third party apps imports


# Local imports
from .models import Admin


# Register your models here.
@admin.register(Admin)
class CustomerModelAdmin(admin.ModelAdmin):
    pass
