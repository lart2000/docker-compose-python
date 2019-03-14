# apps/orders/models.py
# Python imports


# Django imports
from django.db import models
from django.conf import settings

# Third party apps imports
from datetime import datetime

# Local imports


# Create your models here.
class Order(models.Model):
    DRAFT = '00'
    POSTED = '01'
    MATCHED = '02'
    CONFIRM_AND_PAY = '03'
    SHOPPING = '04'
    PAY_SHIPPING = '05'
    DELIVERY = '06'
    DELIVERED = '07'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (POSTED, 'Posted'),
        (MATCHED, 'Matched'),
        (CONFIRM_AND_PAY, 'Confirm & Pay'),
        (SHOPPING, 'Shopping'),
        (PAY_SHIPPING, 'Pay Shipping'),
        (DELIVERY, 'Delivery'),
        (DELIVERED, 'Delivered'),
    )

    name = models.CharField(max_length=50)
    country = models.ForeignKey('countries.Country', models.CASCADE)
    customer = models.ForeignKey('customers.Customer', models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    proxy = models.ForeignKey(
        'proxies.Proxy', models.CASCADE, blank=True, null=True)
    shipping_company = models.CharField(max_length=50, blank=True, null=True)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)

    total_price_proxy = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fee_dope_places = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    final_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=DRAFT)

    def __str__(self):
        return self.customer.user.username

    @property
    def items(self):
        return self.item_set.all()

    @property
    def comments(self):
        return self.comments.all()

    @property
    def total_price(self):
        return sum(self.items.values_list('price', flat=True))


class Comment(models.Model):
    creation_date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    order = models.ForeignKey(
        Order, models.CASCADE, related_name='comments')
    message = models.TextField(blank=True)

    def __str__(self):
        return self.message
