from .models import *
from rest_framework.serializers import ModelSerializer

class AdminSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["full_name","email","password"]

