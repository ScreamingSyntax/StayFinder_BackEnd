from .models import *
from rest_framework import serializers
from customer.serializer import *
from booking.serializers import *
from accomodation.serializer import *
class FetchReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    accommodation = AccommodationAllSerializer()
    booking = FetchBookingSerializer()
    class Meta:
        model = ReviewModel
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = "__all__"



