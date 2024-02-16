from django.db import models
from accomodation.models import *
from customer.models import Customer
from user.models import BaseUser
# Create your models here.
class BookingRequest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Assuming the use of Django's built-in User model
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
    requested_on = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default = False)
    def __str__(self):
        return f"{self.id} {self.user.full_name} - {self.room.accommodation.name} - {self.status}"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    booked_on = models.DateTimeField(auto_now_add=True)
    paid_amount = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.id} {self.user.full_name} - {self.room.accommodation.name} - {self.check_in} to {self.check_out}"

class WhishList(models.Model):
    user = models.ForeignKey(BaseUser,on_delete= models.CASCADE)
    accommodation = models.ForeignKey(Accommodation,on_delete= models.CASCADE)
    is_deleted = models.BooleanField(default=False)