from django.db import models
from django.contrib.auth.models import AbstractUser


class User (AbstractUser):
    CUSTOMER_TYPE='C'
    VENDOR_TYPE='V'
    USER_TYPES={
        
        (CUSTOMER_TYPE,'customer'),
        (VENDOR_TYPE,'vendor'),
    }

    email=models.EmailField(unique=True)
    type=models.CharField(max_length=1 ,choices=USER_TYPES,default=CUSTOMER_TYPE)



class Phone (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='numbers')
    number=models.CharField(max_length=15)


