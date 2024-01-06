from user.models import *
from django.db import models
class Customer(BaseUser):
    image = models.ImageField()