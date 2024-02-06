from django.db import models
from accomodation.models import *
from customer.models import Customer
# Create your models here.
class BookingRequest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Assuming the use of Django's built-in User model
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
    requested_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.full_name} - {self.room.accommodation.name} - {self.status}"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    booked_on = models.DateTimeField(auto_now_add=True)
    paid_amount = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.user.full_name} - {self.room.accommodation.name} - {self.check_in} to {self.check_out}"
