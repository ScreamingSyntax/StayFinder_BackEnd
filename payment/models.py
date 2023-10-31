from django.db import models
from tier.models import Tier
from vendor.models import VendorUser
# Create your models here.
class Payment(models.Model):
    tier_id = models.ForeignKey(Tier,on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey(VendorUser,on_delete=models.DO_NOTHING)
    paid_amount = models.IntegerField(null=False,blank=False)
    method_of_payment = models.CharField(max_length=10,null=False)
    paid_date = models.DateTimeField(auto_now=True)
    paid_till = models.DateTimeField(blank=False,null=False)
    transaction_id = models.TextField(null=True)