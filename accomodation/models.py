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
    image = models.ImageField(upload_to='images/accommodation_images/',null=True)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    longitude= models.CharField(max_length=100)
    latitude =models.CharField(max_length=100)
    type = models.CharField(max_length=20,choices=ACCOMMODATION_TYPES)
    monthly_rate= models.CharField(max_length=20,null=True)
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
class HotelTiers(models.Model):
    accomodation = models.ForeignKey(Accommodation,on_delete=models.CASCADE)
    tier_name = models.CharField(max_length=20)
    description = models.TextField()

class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation,on_delete=models.CASCADE)
    WASHROOM_STATUS = (
        ('exce','Excellent'),
        ('avg','Average'),
        ('adj','Adjustable')

    )
    #For tier based
    seater_beds = models.IntegerField(null=True)
    hotel_tier = models.ForeignKey(HotelTiers,null=True,on_delete=models.CASCADE)
    ac_availability = models.BooleanField(null=True)
    water_bottle_availability = models.BooleanField(null=True)
    steam_iron_availability = models.BooleanField(null=True)
    per_day_rent = models.DecimalField(decimal_places=2,max_digits=6,null=True)
    fan_availability = models.BooleanField()
    bed_availability = models.BooleanField(null=True)
    sofa_availability = models.BooleanField(null=True)
    monthly_rate = models.IntegerField(null=True)
    admission_rate = models.IntegerField(null=True)
    mat_availability = models.BooleanField(null=True)
    carpet_availability = models.BooleanField(null=True)
    washroom_status = models.CharField(max_length=20,choices=WASHROOM_STATUS)
    dustbin_availability = models.BooleanField(null=True)

class RoomImages(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/room_images/')
    