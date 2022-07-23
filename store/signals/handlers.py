from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from store.models.users_models import Customer,Vendor

@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):

    if kwargs['instance'].type =='V':
        kwargs['instance'].is_superuser=True
        kwargs['instance'].is_staff=True

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        if kwargs['instance'].type =='C':
            Customer.objects.create(user=kwargs['instance'])
        elif kwargs['instance'].type =='V':
            Vendor.objects.create(user=kwargs['instance'])