from rest_framework import serializers
from accomodation.models import *

room_fields =  ['fan_availability', 'bed_availability', 'sofa_availability', 'mat_availability', 'carpet_availability', 'washroom_status', 'dustbin_availability',"monthly_rate","seater_beds",]
accommodation_fields = ["name","city","address","image","longitude","latitude","type","monthly_rate","number_of_washroom","trash_dispose_availability","parking_availability","gym_availability","swimming_pool_availability","has_tier","is_verified","is_active","is_pending","vendor","admission_rate","weekly_laundry_cycles","weekly_non_veg_meals","meals_per_day"]
room_image_fields = ['images']
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = room_fields

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = accommodation_fields

class RoomImageSerailizer(serializers.ModelSerializer):
    class Meta:
        model = RoomImages
        fields = room_image_fields

class RoomAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
class RoomAllImageSerailizer(serializers.ModelSerializer):
    class Meta:
        model = RoomImages
        fields = "__all__"

class HotelTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelTiers
        fields = "__all__"
class AllAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = "__all__"

class AllHotelTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelTiers
        fields = "__all__"
class RentRoomSerialzer(serializers.Serializer):
    accommodation = AccommodationSerializer(many=False)
    room_serializer = RoomSerializer(many=False)
    room_images_serializer = RoomImageSerailizer(many=True)
    def create(self,validated_data):
        # print(validated_data)
        accommodation_data = validated_data.pop('accommodation')
        accommodation = Accommodation.objects.create(**accommodation_data)
        room_data = validated_data.pop('room_serializer')
        room = Room.objects.create(accommodation = accommodation, **room_data)
        # room_images_data = print(validated_data)
        room_images_data = validated_data.pop('room_images_serializer')
        print(room_images_data)
        # instances = [RoomImageSerailizer(**room) for room in room_images_data ]
        # print(instances)
        for room_data in list(room_images_data):
            # print(room['images'])
            RoomImages.objects.create(room=room,images = room_data['images'])
    
        # # RoomImages.objects.bulk_create(instances)
        # print(instances)
        # room_images = RoomImages.objects.create(room=room,**room_images_data)
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

# class HotelTierRoomSerializer(serializers.Serializer):
#     room = RoomAllSerializer()
#     images = RoomAllImageSerailizer()
#     def create(self,validated_data):
#         room_data = validated_data.pop('room')
#         room = Room.objects.create(**room_data)
#         image_data = validated_data.pop('image')
#         image = RoomImages.objects.create(room=room,**image_data)
#         return {
#             "room":room,
#             "image":
#         }
class HostelSerializer(serializers.Serializer):
    accommodation = AccommodationSerializer(many=False)
    room = RoomSerializer(many=True)
    def create(self,validated_data):
        accommodation_data = validated_data.pop('accommodation')
        accommodation = Accommodation.objects.create(**accommodation_data)
        
        room_data = validated_data.pop('room')
        for room in room_data:
            Room.objects.create(accommodation=accommodation,**room)

        return{
            'accommodation':accommodation.pk,
        }
class AddHostelRoomSerializer(serializers.Serializer):
    room = RoomSerializer(many=False)
    image = RoomImageSerailizer(many=True)
    def create(self,validated_data):
        print(self.context['accommodation'])
        room_data = validated_data.pop('room')
        room = Room.objects.create(accommodation=self.context['accommodation'] ,**room_data)
        room.save()
        image_data = validated_data.pop('image')
        try:
            for image in image_data:
                image_obj = RoomImages.objects.create(room = room,**image)
                image_obj.save()
        except:
            room.delete()
        return{
         "error":"adad"   
        }
class AddHotelTierSerializer(serializers.Serializer):
    tier = HotelTierSerializer(many=False)
    room = RoomAllSerializer(many=True)

    def create(self,validated_data):
        tier_data = validated_data.pop('tier')
        print(tier_data)
        tier = HotelTiers.objects.create(**tier_data)
        room_data = validated_data.pop('room')
        room_objects = []
        for rooms in room_data:
            room = Room.objects.create(hotel_tier = tier,**rooms)
            room_objects.append(room)
        return {
            "tier":tier,
            "room":room_objects
        }

class AddNonTierHotelSerializer(serializers.Serializer):
    room = RoomAllSerializer(many=True)
    images = RoomImageSerailizer(many=True)

    def create(self,validated_data):
        # print(validated_data)
        room_data = validated_data.pop('room')
        room_list = []
        for room in room_data:
            room_list.append(Room.objects.create(**room))
        # print(room_list)
        image_data = validated_data.pop('images')
        image_list = []
        count = 0
        for image in image_data:
            image_list.append(RoomImages.objects.create(room=room_list[count],**image))
            count+=1
        return{
            'room':room_list,
            'images':image_list
        }
        # room_data = validated_data.pop('room')
class AddNonTierHotelRoomSerializer(serializers.Serializer):
    room = RoomAllSerializer(many=False)
    images=RoomImageSerailizer(many=False)
    def create(self,validated_data):
        room_data = validated_data.pop('room')
        room = Room.objects.create(**room_data)
        image_data = validated_data.pop('images')
        image = RoomImages.objects.create(room=room,**image_data)
        return {
            'room':room,
            'images':image
        }