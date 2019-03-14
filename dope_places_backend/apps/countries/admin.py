# apps/countries/admin.py
# Python imports


# Django imports
from django.contrib import admin


# Third party apps imports
from import_export.admin import ImportExportActionModelAdmin


# Local imports
from .models import Country


# Register your models here.
@admin.register(Country)
class CountryModelAdmin(ImportExportActionModelAdmin):
    pass
