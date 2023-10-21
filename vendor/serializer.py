from vendor.models import VendorUser
from rest_framework.serializers import ModelSerializer

class VendorSerializer(ModelSerializer):
    class Meta:
        model = VendorUser
        fields = "__all__"