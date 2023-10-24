from django.db import models
from vendor.models import VendorUser
class Tier(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=False)
    price = models.CharField(max_length=20)
    accomodationLimit = models.IntegerField()

    def __str__(self):
        return self.name

class CurrentTier(models.Model):
    tier = models.ForeignKey(Tier,on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorUser,on_delete=models.CASCADE,related_name='vendor_tier')
    paid_amount = models.CharField(null=False)
    paid_date = models.DateTimeField()
    is_active = models.BooleanField()
    
    def __str__(self):
        return f"{self.vendor.full_name} : {self.tier.name}"