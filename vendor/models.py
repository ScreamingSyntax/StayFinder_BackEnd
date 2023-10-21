from django.db import models
from user.models import BaseUser
from django.utils import timezone
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
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    date_verified = models.DateTimeField(null=True)