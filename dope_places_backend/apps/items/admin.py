# apps/items/admin.py
# Python imports


# Django imports
from django.contrib import admin

# Third party apps imports


# Local imports
from .models import Item


# Register your models here.
@admin.register(Item)
class ItemModelAdmin(admin.ModelAdmin):
    pass
