from .models import *
from rest_framework.serializers import ModelSerializer

class AdminSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["full_name","email"]

class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["full_name","email","id","phone_number","user_type"]