from rest_framework import serializers
from accomodation.models import *

room_fields =  ['fan_availability', 'bed_availability', 'sofa_availability', 'mat_availability', 'carpet_availability', 'washroom_status', 'dustbin_availability']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = room_fields

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ["name","city","address","image","longitude","latitude","type","monthly_rate","number_of_washroom","trash_dispose_availability","parking_availability","gym_availability","swimming_pool_availability","has_tier","is_verified","is_active","is_pending","vendor"]


class RentRoomSerialzer(serializers.Serializer):
    accommodation = AccommodationSerializer(many=False)
    room_serializer = RoomSerializer(many=False)
    def create(self,validated_data):
        # print(validated_data)
        accommodation_data = validated_data.pop('accommodation')
        accommodation = Accommodation.objects.create(**accommodation_data)
        room_data = validated_data.pop('room_serializer')
        room = Room.objects.create(accommodation = accommodation, **room_data)
        return {
            'accommodation':accommodation,
            'room':room
        }
    
# class RentRoomSerialzer(serializers.Serializer):
#     room_serializer = RoomSerializer()
#     accommodation_serializer = AccommodationSerializer()
#     def create(self,validated_data):
#         accommodation_data = validated_data.pop('accommodation')
#         accommodation = Accommodation.objects.create(**accommodation_data)
#         room_data = validated_data.pop('room')
#         instances = [RoomSerializer(**room) for room in room_data ]
#         Room.objects.bulk_create(instances)
#         # room = Room.objects.create(accommodation = accommodation, **room_data)
#         return {
#             'accommodation':accommodation
#         }