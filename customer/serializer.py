from customer.models import *
from rest_framework.serializers import ModelSerializer

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ["full_name","email","password","image"]
