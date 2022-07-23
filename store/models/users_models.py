from django.db import models
from django.conf import settings



class Customer (models.Model):
    FEMALE='F'
    MALE='M'
    
    GENDER_CHOICES={
        (MALE,'male'),
        (FEMALE,'female')
    }
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES,default=MALE)
    birth_date=models.DateField(null=True,blank=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='customer')


    def first_name(self):
        return self.user.first_name


    def last_name(self):
        return self.user.last_name
    
    def user_name(self):
        return self.user.username

    def __str__(self) -> str:
        return f'{self.first_name()} {self.last_name()}' 


class Vendor(models.Model):
    store_name=models.CharField(max_length=50)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='vendor')


    def first_name(self):
        return self.user.first_name


    def last_name(self):
        return self.user.last_name
        
    def user_name(self):
        return self.user.username
        
    def __str__(self) -> str:
        return f'{self.first_name()} {self.last_name()}' 

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
