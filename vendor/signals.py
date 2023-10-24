from django.dispatch import receiver
from vendor.models import *
from django.db.models.signals import post_save
@receiver(post_save,sender=VendorUser)
def create_function(sender,instance,created,**kwargs):
    if created:
        VendorProfile.objects.create(vendor = instance)

@receiver(post_save,sender=VendorUser)
def save_profile(sender,instance,**kwargs):
    instance.vendor_profile.save()