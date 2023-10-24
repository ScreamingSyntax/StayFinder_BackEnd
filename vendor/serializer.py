from vendor.models import *
from rest_framework.serializers import ModelSerializer

class VendorSerializer(ModelSerializer):
    class Meta:
        model = VendorUser
        fields = "__all__"

class VendorProfileSerializer(ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = "__all__"