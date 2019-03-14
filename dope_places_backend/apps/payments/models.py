# apps/orders/models.py
# Python imports
from decimal import Decimal

# Django imports
from django.db import models


# Third party apps imports


# Local imports
from apps.orders.models import Order


# Create your models here.
class PaymentPaypalManager(models.Manager):
    def create_payment(self, payment_id, order):
        payment = self.create\
            (order=order,
             payment_id=payment_id,
             precio=order.final_price)
        return payment


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    payment_id = models.CharField(max_length=64, db_index=True)
    payer_id = models.CharField(max_length=128, blank=True, db_index=True)
    payer_email = models.EmailField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    is_paid = models.BooleanField(default=False)
    objects = PaymentPaypalManager()
