from django.db import models
from accomodation.models import Accommodation
from customer.models import Customer
from booking.models import Booking
class ReviewModel(models.Model):
    # Title is for ratings 1-5
    title = models.DecimalField(decimal_places=1,max_digits=2)
    description = models.TextField()
    image = models.ImageField(upload_to='reviews/',null=True)
    accommodation = models.ForeignKey(Accommodation,models.CASCADE)
    customer = models.ForeignKey(Customer,models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    added_time = models.DateTimeField(auto_now=True,null=False)
    booking = models.ForeignKey(Booking,models.CASCADE,null = True)
    def __str__(self):
        return f"{self.id} - {self.accommodation.name} - {self.customer.full_name}" 
    