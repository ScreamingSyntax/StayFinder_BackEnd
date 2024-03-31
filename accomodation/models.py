from django.db import models
from vendor.models import VendorUser
class Accommodation(models.Model):
    ACCOMMODATION_TYPES = (
        ('hostel','Hostel'),
        ('hotel','Hotel'),
        ('rent_room','rent_room'),
    )  
    vendor = models.ForeignKey(VendorUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='accommodation_images/',null=True)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    longitude= models.CharField(max_length=100)
    latitude =models.CharField(max_length=100)
    type = models.CharField(max_length=20,choices=ACCOMMODATION_TYPES)
    monthly_rate= models.IntegerField(null=True)
    number_of_washroom = models.IntegerField(null=True)
    trash_dispose_availability = models.BooleanField(null=True)
    parking_availability = models.BooleanField(null=True)
    gym_availability = models.BooleanField(null=True)
    swimming_pool_availability = models.BooleanField(null=True)
    has_tier = models.BooleanField(null=True)
    date_added =models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(null=True)
    is_pending = models.BooleanField(default=True)
    meals_per_day = models.IntegerField(null=True)
    weekly_non_veg_meals = models.IntegerField(null=True)
    weekly_laundry_cycles = models.IntegerField(null=True)  
    admission_rate = models.IntegerField(null=True)
    is_rejected = models.BooleanField(default=False)
    # rejected_message = models.Te
    def __str__(self):
        return f"{self.pk} {self.name} {self.vendor.full_name} {self.type}"

class HotelTiers(models.Model):
    accommodation = models.ForeignKey(Accommodation,on_delete=models.CASCADE)
    tier_name = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField()
    
class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation,on_delete=models.CASCADE)
    WASHROOM_STATUS = (
        ('Excellent','excellent'),
        ('Average','average'),
        ('Adjustable','adjustable')
    )
    seater_beds = models.IntegerField(null=True)
    hotel_tier = models.ForeignKey(HotelTiers,null=True,on_delete=models.CASCADE)
    ac_availability = models.BooleanField(null=True)
    water_bottle_availability = models.BooleanField(null=True)
    steam_iron_availability = models.BooleanField(null=True)
    per_day_rent = models.IntegerField(null=True)
    fan_availability = models.BooleanField()
    bed_availability = models.BooleanField(null=True)
    sofa_availability = models.BooleanField(null=True)
    monthly_rate = models.IntegerField(null=True)
    mat_availability = models.BooleanField(null=True)
    carpet_availability = models.BooleanField(null=True)
    washroom_status = models.CharField(max_length=20,choices=WASHROOM_STATUS,null=True)
    dustbin_availability = models.BooleanField(null=True)
    kettle_availability = models.BooleanField(null=True)
    coffee_powder_availability  = models.BooleanField(null=True)
    milk_powder_availability  = models.BooleanField(null=True)
    tea_powder_availability  = models.BooleanField(null=True)
    hair_dryer_availability = models.BooleanField(null=True)
    tv_availability = models.BooleanField(null=True)
    room_count = models.IntegerField(default=0)
     
    def __str__(self):
        return f"{self.pk} {self.accommodation.name} {self.accommodation.vendor.full_name}"
    
class RoomImages(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f" {self.pk}  {self.room.accommodation.name} {self.room.accommodation.vendor.full_name}"