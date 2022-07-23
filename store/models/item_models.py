from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator

from store.models.users_models import  Vendor


class Category (models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField()


class Item (models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='items')
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE , related_name='item')
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together=[['cart','item']]
