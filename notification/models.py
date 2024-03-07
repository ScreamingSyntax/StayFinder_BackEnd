from django.db import models
from customer.models import Customer
from vendor.models import  VendorUser
# from customer.models import Customer
from user.models import BaseUser
import datetime
class Notification(models.Model):
    customer = models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorUser,null=True,on_delete=models.CASCADE)
    description = models.CharField(max_length = 100)
    TARGET = (
        ('all','All'),
        ('customer','Customer'),
        ('vendor','Vendor')
    )
    TYPES = (
        ('warning','Warning'),
        ('info','Info'),
        ('success','Success'),
        ('failure','Failure'),)
    is_seen = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20,choices = TYPES,null=True)
    target = models.CharField(max_length=20,choices = TARGET,null=True)
    added_date = models.DateTimeField(default=datetime.datetime.now())

class NotificationDevice(models.Model):
    user = models.ForeignKey(BaseUser,on_delete=models.CASCADE)
    device_id = models.TextField()
    # is_banned = models.Boole
    device_model = models.CharField(max_length=50,null=True,default='Unknown')

