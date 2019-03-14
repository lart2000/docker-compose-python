# apps/items/models.py
# Python imports


# Django imports
from django.db import models


# Third party apps imports


# Local imports


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50)
    order = models.ForeignKey(
        'orders.Order', models.CASCADE, blank=True, null=True)
    link = models.CharField(max_length=500)
    notes = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    notes_proxy = models.TextField(blank=True, null=True)
    price_proxy = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    @property
    def photos(self):
        return self.photos.all()

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=50, blank=True)
    item = models.ForeignKey(
        Item, models.CASCADE, blank=True, null=True, related_name='photos')

    def __str__(self):
        return self.item.name
