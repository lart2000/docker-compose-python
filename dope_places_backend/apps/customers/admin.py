# apps/customers/admin.py
# Python imports


# Django imports
from django.contrib import admin


# Third party apps imports


# Local imports
from .models import Customer, PasswordToken


# Register your models here.
@admin.register(Customer)
@admin.register(PasswordToken)
class CustomerModelAdmin(admin.ModelAdmin):
    pass
