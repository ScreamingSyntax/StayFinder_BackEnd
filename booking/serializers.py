from rest_framework import serializers
from .models import *
from accomodation.serializer import *
from customer.serializer import *
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'user', 'check_in', 'check_out', 'booked_on','paid_amount']

    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)
        return booking

class WishListSerializer(serializers.ModelSerializer):
    accommodation = AccommodationAllSerializer()
    class Meta:
        model = WhishList
        fields = "__all__"

class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = ['id', 'room', 'user', 'status',"requested_on"]

    def create(self, validated_data):
        booking_request = BookingRequest.objects.create(**validated_data)
        return booking_request

class FetchBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'user', 'check_in', 'check_out', 'booked_on','paid_amount']

class RoomWithAccommodationSerializer(serializers.ModelSerializer):
    accommodation = AccommodationAllSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'seater_beds', 'per_day_rent', 'accommodation',"monthly_rate"]

class FetchBookingSerializer(serializers.ModelSerializer):
    room = RoomWithAccommodationSerializer()
    user = CustomerSerializer()
    class Meta:
        model = Booking
        fields = ['id', 'room', 'user', 'check_in', 'check_out', 'booked_on', 'paid_amount']


class FetchBookingRequestSerializer(serializers.ModelSerializer):
    room = RoomWithAccommodationSerializer()
    user = CustomerSerializer()

    class Meta:
        model = BookingRequest
        fields = ['id', 'room', 'user', 'status', "requested_on"]