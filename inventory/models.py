from django.db import models
from accomodation.models import Accommodation 
from django.utils import timezone 

class Inventory(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)

def current_date():
    return timezone.now().date()

class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  
    image = models.ImageField()
    count = models.IntegerField()
    price = models.IntegerField()
    date_field = models.DateField(default = current_date)
    is_deleted = models.BooleanField(default=False)

class InventoryLogs(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)  
    STATUS_CHOICES = ( 
        ('added', 'Added'),
        ('removed', 'Removed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    count = models.IntegerField(null=True)