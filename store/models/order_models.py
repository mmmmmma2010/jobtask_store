from uuid import uuid4
from django.db import models
from django.conf import settings
from store.models.users_models import Customer
from .item_models import Item
from django.core.validators import MinValueValidator




class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions=[
            ('cancel_order','Can Cancel Order')
        ]

class OrderItem(models.Model):
    SHIPPING_STATUS_PENDING = 'P'
    SHIPPING_STATUS_SHIPPED = 'C'
    SHIPPING_STATUS_DELVIRED = 'F'
    SHIPPING_STATUS_CHOICES = [
        (SHIPPING_STATUS_PENDING, 'Pending'),
        (SHIPPING_STATUS_SHIPPED, 'Shipped'),
        (SHIPPING_STATUS_DELVIRED, 'Deliverded')
    ]

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_state= models.CharField(max_length=1, choices=SHIPPING_STATUS_CHOICES,default=SHIPPING_STATUS_PENDING)




        