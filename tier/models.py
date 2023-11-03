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
    
class TierTransaction(models.Model):
    vendor = models.ForeignKey(VendorUser, on_delete=models.CASCADE, related_name='transactions')
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    method_of_payment = models.CharField(max_length=20)
    paid_date = models.DateTimeField(auto_now=True)
    paid_till = models.DateTimeField()
    transaction_id = models.TextField() 
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.vendor.full_name} : {self.tier.name}"
    