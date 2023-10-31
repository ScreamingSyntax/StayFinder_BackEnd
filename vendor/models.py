from django.db import models
from user.models import BaseUser
# class VendorUser(AbstractUser):
#     username=None
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=10)
#     USERNAME_FIELD="email"
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         blank=True,
#         related_name='vendors'  # You can choose a meaningful name here
#     )
#     groups = models.ManyToManyField(
#         'auth.Group',
#         blank=True,
#         related_name='vendor_groups'
#     )
    
#     def __str__(self):
#         return self.full_name

class VendorUser(BaseUser):
    date_joined = models.DateTimeField(auto_now=True)
    date_verified = models.DateTimeField(null=True)
    def __str__(self):
        return self.email
class VendorProfile(models.Model):
    is_under_verification_process = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    vendor= models.OneToOneField(VendorUser,on_delete=models.CASCADE,related_name="vendor_profile")
    profile_picture=models.ImageField(default='profile_pic.png')
    citizenship_back = models.ImageField(default='citizenship_back.jpeg')
    citizenship_front = models.ImageField(default='citizenship_front.jpeg')
    digital_signature = models.ImageField(default='signature.png')
    is_rejected = models.BooleanField(default=False)
    rejected_message = models.CharField(max_length=50,null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.vendor.email