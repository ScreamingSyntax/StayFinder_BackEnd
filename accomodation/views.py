from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from tier.models import Tier,TierTransaction
from accomodation.serializer import *
from collections import namedtuple
import json
Rent = namedtuple('Rent',('accommodation','room_serializer','room_image_serializer'))
Hostel = namedtuple('Hotel',('accommodation','room'))
from collections import OrderedDict


class RentalRoomImage(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self,request):
         if request.user.is_authenticated:
            try:
                if 'room_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide the room you want to update"
                    })
                if 'room_image_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide the room image id you want to update"
                    })
                if 'image' not in request.data:
                     return Response({
                        "success":0,
                        "message":"You need to provide the image you want to update"
                    })
                room = Room.objects.get(id=request.data['room_id'])
                roomImage = RoomImages.objects.get(id=request.data['room_image_id']);
                roomImage.images = request.data['image'];
                roomImage.save()
                if  room.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The rental room doesn't belong to you"
                    })
                if roomImage.room != room:
                    return Response({
                        "success":0,
                        "message":"The image doesn't belong to the room"
                    })
                
                if room.accommodation.type != 'rent_room':
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a rental room"
                    })
                
                return Response({
                    "success":1,
                    "message":"Coming soon"
                })
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except RoomImages.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })

class RentalRoomRoomUpdate(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self,request):
         if request.user.is_authenticated:
            try:
                if 'room_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide the room you want to update"
                    })
                room = Room.objects.get(id=request.data['room_id'])
                # roomImage.save()
                if  room.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The rental room doesn't belong to you"
                    })
                
                if room.accommodation.type != 'rent_room':
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a rental room"
                    })
                roomSerializer = RoomSerializer(room,data=request.data,partial=True)
                # room.save()
                if roomSerializer.is_valid():
                    roomSerializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully Updated"
                    })
                return Response({
                    "success":0,
                    "message":"Server Error"
                })
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except RoomImages.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
class RentalRoom(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self,request):
        if request.user.is_authenticated:
            try:
                if 'accommodation' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide the accommodation you want to delete"
                    })
                accommodation = Accommodation.objects.get(id=request.data['accommodation'])
                if accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The rental room doesn't belong to you"
                    })
                if accommodation.type != 'rent_room':
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a rental room"
                    })
                accommodation.delete()
                return Response({
                    "success":1,
                    "nessage":"Successfully deleted"
                })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
    def patch(self,request):
        if request.user.is_authenticated:
            try:
                if 'accommodation[id]' not in request.data:
                    return Response({
                        'success':0,
                        'message':"You should provide the id of the accommodation you want to update"
                    })
                accommodation = Accommodation.objects.get(id=request.data['accommodation[id]'])
                if(accommodation.vendor.email  != request.user.email):
                    return Response({
                        "success":0,
                        "message":"You are not allowed to update this"
                    })
                mapping={
                    "accommodation":{},
                }
                accommodation_fields = ["id","name", "city", "address", "longitude", "latitude", "type",
                            "number_of_washroom", "trash_dispose_availability",
                            "parking_availability", "monthly_rate", "image"]
                for field in accommodation_fields:
                    if f"accommodation[{field}]" in request.data:
                        mapping['accommodation'][field] = request.data.get(f'accommodation[{field}]')
                if(mapping['accommodation'] != {}):
                    accommodation_serializer = AccommodationSerializer(accommodation,data = mapping['accommodation'],partial=True)
                    if accommodation_serializer.is_valid():
                        accommodation_serializer.save()
                        return Response({
                            "success":1,
                            "message":"Successfully Updated"
                        })
                    else:
                        return Response({
                            "success":0,
                            "message":accommodation_serializer.errors
                        })

                # return Response({
                #     "success":0,
                #     "message":"Under Construction"
                # })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
            except:
                return Response({"success":0,
                                "message":"Please verify your data"})
    def get(self,request):
        if request.user.is_authenticated:
            try:
                accommodation  = Accommodation.objects.get(id=request.data['accommodation'],vendor=request.user)
                if(accommodation.type != 'rent_room'):
                    return Response({
                        "success":0,
                        "message":"This is not a rental room"
                    })
                room_data= Room.objects.get(accommodation=accommodation)
                room_images_data = RoomImages.objects.filter(room = room_data)
                accommodation_serializer = AccommodationAllSerializer(accommodation)
                room_serializer = RoomAllSerializer(room_data)
                room_image_serializer = RoomAllImageSerailizer(room_images_data,many=True)
                return Response({
                    "success":1,
                    "data":{
                        "accommodation":accommodation_serializer.data,
                        "room":room_serializer.data,
                        "room_images": room_image_serializer.data
                    }
                })
        
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something went wrong"
                })
    def post(self, request):
            errors ={}
            if request.user.is_authenticated:
                required_fields = [
                "accommodation[name]",
                "accommodation[city]",
                "accommodation[address]",
                "accommodation[longitude]",
                "accommodation[latitude]",
                "accommodation[type]",
                "accommodation[number_of_washroom]",
                "accommodation[trash_dispose_availability]",
                "accommodation[parking_availability]",
                "accommodation[monthly_rate]",
                "accommodation[image]",
                "room[fan_availability]",
                "room[bed_availability]",
                "room[sofa_availability]",
                "room[mat_availability]",
                "room[carpet_availability]",
                "room[washroom_status]",
                "room[dustbin_availability]",
                "room_image[0]",
                "room_image[1]",
                "room_image[2]",
            ]
            for field in required_fields:
                value = request.data.get(field)
                if value is None or value == "":
                    errors[field] = f"{field}"
                    return Response({
                    "success":0,
                    "message":f"The field {errors[field]} is required" 
                })
            mapping = {
                 "accommodation": {
                     "name": request.data.get('accommodation[name]'),
                     "city": request.data.get('accommodation[city]'),
                     "address": request.data.get('accommodation[address]'),
                     "longitude": request.data.get('accommodation[longitude]'),
                     "latitude": request.data.get('accommodation[latitude]'),
                     "type": request.data.get('accommodation[type]'),
                     "number_of_washroom": request.data.get('accommodation[number_of_washroom]'),
                     "trash_dispose_availability": request.data.get('accommodation[trash_dispose_availability]'),
                     "parking_availability": request.data.get('accommodation[parking_availability]'),
                     "monthly_rate": request.data.get('accommodation[monthly_rate]'),
                     "image":request.data.get('accommodation[image]'),
                    #  "description":request.data.get('accommodation[description]')
                 },
                 "room": {
                     "fan_availability": request.data.get('room[fan_availability]'),
                     "bed_availability": request.data.get('room[bed_availability]'),
                     "sofa_availability": request.data.get('room[sofa_availability]'),
                     "mat_availability": request.data.get('room[mat_availability]'),
                     "carpet_availability": request.data.get('room[carpet_availability]'),
                     "washroom_status": request.data.get('room[washroom_status]'),
                       "dustbin_availability": request.data.get('room[dustbin_availability]'),
                     },
                'room_image':[
                    {
                        'images': request.data.get('room_image[0]')
                    },
                    {
                        'images': request.data.get('room_image[1]')
                    },
                    {
                        'images': request.data.get('room_image[2]')
                    },
                    
                ]
            }
            mapping['accommodation']['vendor'] = request.user
            mapping['room']['accommodation'] = mapping['accommodation']
            print(mapping)
            rent = Rent(
                accommodation= mapping['accommodation'],
                room_serializer=mapping['room'],
                room_image_serializer=mapping['room_image'],
            )
            serializer = RentRoomSerialzer(data={'accommodation': rent.accommodation, 'room_serializer': rent.room_serializer,'room_images_serializer':rent.room_image_serializer})
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": 1,
                    "message": "Successfully added"
                })
            else:
                print(serializer.errors)
                return Response({
                    "success": 0,
                    "message": "Validation errors occurred"
                })

class ShowAccommodations(APIView):
    def get(self,request):
        try:
            accommodation = Accommodation.objects.all()
            accommodation_serializer = AccommodationAllSerializer(accommodation,many=True)
            return Response({
                "success":1,
                "data":accommodation_serializer.data
            })
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"Accommodation Doesn't exist"
            })
class ShowParticularAccommodation(APIView):
    def get(self,request):
        try:
            param_value = request.query_params.get('id', None)
            if param_value == None:
                return Response({
                    "success":0,
                    "message":"Please provide product id"
                })
            accommodation = Accommodation.objects.get(id=param_value)
            print(accommodation.type)
            print(accommodation.has_tier)
            accommodation_serializer = AccommodationAllSerializer(accommodation,many=False)
            if(accommodation.type in ["hotel","rent_room","hostel"] and accommodation.has_tier in [None,False]):
                room = Room.objects.filter(accommodation=accommodation)
                room_serializer = FetchRoomsWithImages(room,many=True)
                return Response({
                    "success":1,
                    "data":{
                        "accommodation":accommodation_serializer.data,
                        "rooms":room_serializer.data
                    }
                })
            if(accommodation.type =="hotel" and accommodation.has_tier == True):
                hotel_tier = HotelTiers.objects.filter(accommodation=accommodation)
                hotel_tier_serializer = FetchTierWithRooms(hotel_tier,many=True)
                return Response({
                    "success":1,
                    "data":{
                        "accommodation":accommodation_serializer.data,
                        "tier":hotel_tier_serializer.data
                    }
                })
            
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"Accommodation Doesn't exist"
            })
class AccommodationView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self,request):
        if request.user.is_authenticated:
            try:
                if 'accommodation_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"Please provide accommodation id to delete"
                    })
                data = request.data['accommodation_id']
                if data == None or data =="":
                    return Response({
                        "success":0,
                        "message":"The accommodation id cannot be null"
                    })
                accommodation = Accommodation.objects.get(id=request.data['accommodation_id'])
                if accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The accommodation doesn't belong to you"
                    })
                accommodation.delete()
                return Response({
                    "success":1,
                    "message":"The accommodation is successfully deleted"
                })
            except  Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
    def get(self,request):
        if request.user.is_authenticated:
            try:
                accommodation = Accommodation.objects.filter(vendor=request.user)
                print(accommodation)
                accommodation_serializer = AccommodationAllSerializer(accommodation,many=True)
                return Response({
                    "success":1,
                    "data":accommodation_serializer.data
                })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"Accommodation Doesn't exist"
                })
class VerifyAccommodation(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if request.user.is_authenticated:
            try:
                if 'accommodation' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide accommodation id"
                    })
                accommodation = Accommodation.objects.get(id = request.data["accommodation"])
                # print(accommodation.is_verified)
                if accommodation.is_verified:
                    return Response({
                        "success":0,
                        "message":"The accommodation is already verified"
                    })
                accommodation.is_verified=True
                accommodation.save()
                return Response({
                    "success":0,
                    "message":"Sucessfully Verified"
                })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })

class HostelImageRooms(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def patch(self,request):
        if request.user.is_authenticated:
            try:
                print(request.data)
                if 'room_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide the room you want to update"
                    })
                if 'room_image_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide the room image id you want to update"
                    })
                if 'image' not in request.data:
                     return Response({
                        "success":0,
                        "message":"You need to provide the image you want to update"
                    })
                room = Room.objects.get(id=request.data['room_id'])
                roomImage = RoomImages.objects.get(id=request.data['room_image_id']);
                roomImage.images = request.data['image'];
                roomImage.save()
                if  room.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The rental room doesn't belong to you"
                    })
                if roomImage.room != room:
                    return Response({
                        "success":0,
                        "message":"The image doesn't belong to the room"
                    })
                
                if room.accommodation.type != 'hostel':
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a hostel room"
                    })
                
                return Response({
                    "success":1,
                    "message":"Successfully Done"
                })
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except RoomImages.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
class HostelRooms(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def get(self,request):
        if request.user.is_authenticated:
            try:
                if 'id' not in request.data:
                        return Response({
                            "success":0,
                            "message":"You should provide room id"
                        })
                print(request.data['id'])
                accommodation = Accommodation.objects.get(id=request.data['id'])
                if accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The room doesn't belong to you"
                    })
                if accommodation.type != "hostel":
                    return Response({
                        "success":0,
                        "message":"The accomodation isn't a hostel"
                    })
                room = Room.objects.filter(accommodation=accommodation)
                room_serializer = RoomAllSerializer(room,many=True)
                room_id = []
                for room in room:
                    room_id.append(room.pk)
                room_image = RoomImages.objects.filter(room__in=room_id)
                room_image_serializer = RoomAllImageSerailizer(
                    room_image,many=True
                )
                return Response({
                        "success":1,
                        "data":{
                        "rooms":room_serializer.data,
                        "room_image":room_image_serializer.data
                        }
                    })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"Room doesn't exist"
                })
    # def get(self)
    def delete(self,request):
        if request.user.is_authenticated:
            
            try:
                if 'id' not in request.data:
                        return Response({
                            "success":0,
                            "message":"You should provide room id"
                        })
                print(request.data['id'])
                room = Room.objects.get(id=request.data['id'])
                if room.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The room doesn't belong to you"
                    })
                if room.accommodation.type != "hostel":
                    return Response({
                        "success":0,
                        "message":"The accomodation isn't a hostel"
                    })
                room.delete()
                return Response({
                    "success":1,
                    "message":"Successfully Deleted"
                })
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"Room doesn't exist"
                })
    def patch(self,request):
        if request.user.is_authenticated:
            try:
                if 'id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You should provide room id"
                    })
                room = Room.objects.get(id = request.data['id'])
                type = room.accommodation.type
                print(type)
                # accommodation = Room.objects.get(accommodation_id=room)
                if type != 'hostel':
                    return Response({
                        "success":0,
                        "message": "The room isn't a hostel"
                    })
                mapping = {
                    'room':{},
                  
                }
          
                room_fields =  ['fan_availability', 'monthly_rate','washroom_status',"seater_beds"]
               
                for field in request.data:
                    if field in room_fields:
                        mapping["room"][field] = request.data.get(field)
                   
                mapping['room']['accommodation'] = room.accommodation.pk
                mapping["room"]['id'] = room.pk
                room_serializer = RoomAllSerializer(instance=room,data= mapping['room'],partial=True)
                if room_serializer.is_valid():
                    room_serializer.save()
                    return Response({
                        'success':1,
                        "message":"Successfully Done :)"
                    })
                else:
                    return Response({
                        "success":0,
                        "message":room_serializer.errors
                    })
                return Response({
                    "success":0,
                    "message":"Coming soong"
                })
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"Room doesn't exit"
                })
    def post(self,request):
        if request.user.is_authenticated:
            try:
                if 'accommodation_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"Please provide accommodation id"
                    })
                accommodation = Accommodation.objects.get(id=request.data['accommodation_id'])
                if accommodation.type != 'hostel':
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a hostel"
                    })
                required_fields =  {"fan_availability",
                    "monthly_rate",
                    "seater_beds",
                    "washroom_status",
                    "image_1",
                    "image_2"
                    }
                required_data = {}
                for data in required_fields:
                    if data not in request.data:
                        return Response({
                            "success":0,
                            "message":f"Hey there, I think you are missing {data} field"
                        })
                    if data in request.data:
                        fields = request.data[data]
                        if(fields == None or fields =="" ):
                            return Response({
                                "success":0,
                                "message":f"Hey there, The field {data} cannot be null"
                            })
                        required_data[data]=fields
                required_data['accommodation'] = accommodation.pk
                room = AddHostelRoomSerializer(data={'room':required_data,'image':[{'images':required_data['image_1']}, {'images':required_data['image_2']}]},context={'accommodation':accommodation})
                if room.is_valid():
                    room.save()
                    return Response({
                        "success":1,
                        "message":"Successfully added"
                    })
                # print(serializers.err)
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Please verify your data before sending it :>"
                })
class HostelAccommodation(APIView):
    authentication_classes=[SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self,request):
        if request.user.is_authenticated:
            try:
                if('id' not in request.data):
                    return Response({
                        "success":0,
                        "message":"Please mention the hostel you want to delete"
                    })
                accommodation = Accommodation.objects.get(id=request.data['id'])
                if(accommodation.type != 'hostel'):
                        return Response({
                            "success":0,
                            "message":"The accommodation isn't a hostel"
                        })
                if(accommodation.vendor.email != request.user.email):
                    return Response({
                        "success":0,
                        "message":"The accommodation doesn't belong to you"
                    })
                accommodation.delete()
                return Response({
                    "success":1,
                    "message":"Successfully deleted"
                })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
    def get(self,request):
        if request.user.is_authenticated:
            try:
                if('id' not in request.data):
                    return Response({
                        "success":0,
                        "message":"Please provide accommodation id"
                    })
                accommodation = Accommodation.objects.get(id=request.data['id'])
                if(accommodation.type != 'hostel'):
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a hostel"
                    })
                room = Room.objects.filter(accommodation=accommodation)
                accommodation_serializer = AccommodationSerializer(accommodation)
                room_serializer = RoomAllSerializer(room,many=True)
                room_id = []
                for room in room:
                    room_id.append(room.pk)
                room_image = RoomImages.objects.filter(room__in=room_id)
                room_image_serializer = RoomAllImageSerailizer(room_image,many=True)
                return Response({
                    "success":1,
                    "data":{
                        'accommodation':accommodation_serializer.data,
                        'room':room_serializer.data,
                        'images':room_image_serializer.data
                    }
                })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something went wrong"
                })
  
            
    def post(self,request):
        try:
            
            if request.user.is_authenticated:
                required_fields = [
                    "accommodation[name]",
                    "accommodation[city]",
                    "accommodation[address]",
                    "accommodation[longitude]",
                    "accommodation[latitude]",
                    "accommodation[type]",
                    "accommodation[number_of_washroom]",
                    "accommodation[parking_availability]",
                    "accommodation[image]",
                    "accommodation[type]",
                    "accommodation[admission_rate]",
                    'accommodation[meals_per_day]',
                    'accommodation[weekly_non_veg_meals]',
                    'accommodation[weekly_laundry_cycles]',
                    "room[0][fan_availability]",
                    "room[0][monthly_rate]",
                    "room[0][seater_beds]",
                    "room[0][washroom_status]",
                    "room_image[0][1]",
                    "room_image[0][2]",
                    "accommodation[meals_per_day]",
                    "accommodation[weekly_non_veg_meals]",
                    "accommodation[weekly_laundry_cycles]",
                    "accommodation[admission_rate]"
                ]
                for field in required_fields:
                    if field not in request.data:
                        return Response({
                            "success":0,
                            "message":f"The field {field}  is required"
                        })
                    if field in request.data:
                        data = request.data.get(field)

                        if data is None or data == "":
                            return Response({
                                "success":0,
                                "message":f"The field {field} cannot be null or empty"
                            })
                mapping = {
                     "accommodation": {
                         "name": request.data.get('accommodation[name]'),
                         "city": request.data.get('accommodation[city]'),
                         "address": request.data.get('accommodation[address]'),
                         "longitude": request.data.get('accommodation[longitude]'),
                         "latitude": request.data.get('accommodation[latitude]'),
                         "type": request.data.get('accommodation[type]'),
                         "number_of_washroom": request.data.get('accommodation[number_of_washroom]'),
                         "parking_availability": request.data.get('accommodation[parking_availability]'),
                         "monthly_rate": request.data.get('accommodation[monthly_rate]'),
                         "image":request.data.get('accommodation[image]'),
                         "meals_per_day":request.data.get('accommodation[meals_per_day]'),
                         "weekly_non_veg_meals":request.data.get('accommodation[weekly_non_veg_meals]'),
                         "weekly_laundry_cycles":request.data.get('accommodation[weekly_laundry_cycles]'),
                         "admission_rate":request.data.get('accommodation[admission_rate]'),
                         "vendor":request.user.pk,
                         "meals_per_day":request.data.get('accommodation[meals_per_day]'),
                         "weekly_non_veg_meals":request.data.get('accommodation[weekly_non_veg_meals]'),
                         "weekly_laundry_cycles":request.data.get('accommodation[weekly_laundry_cycles]'),
                     },
                     "room": [],
                     "room_images":[]
                }  
                room_data = {}  

                for key, value in request.POST.items():
                    if key.startswith("room["):

                        room_index = int(key.split("[")[1].split("]")[0])
                        field_name = key.split("][")[1].rstrip("]")

                        if room_index not in room_data:
                            room_data[room_index] = {}
                        room_data[room_index][field_name] = value
                required_field = ['fan_availability','washroom_status','seater_beds','monthly_rate']          
                for key,room in room_data.items():
                    for field in required_field:
                        if room.get(field) is None:
                            return Response({
                                "success" :0,
                                "message": f"{field} field is required in room {key}"
                            })
                    mapping["room"].append(room)
                hostel = Hostel(
                    accommodation=mapping["accommodation"],
                    room=mapping["room"]
                )
                room_image_data = []
                for key, value in request.data.items():
                    if key.startswith("room_image["):

                        room_image_index = int(key.split("[")[1].split("]")[0])
                        field_name = key.split('[')[0]
                        room_image_data.append({'image' :value})
                if(len(room_image_data) != 2* len(hostel.room)):
                    return Response({
                        "success":0,
                        "message":"Room Images aren't enough"
                    })
                serializer = HostelSerializer(data={'accommodation':mapping['accommodation'],'room':mapping['room']})
                if serializer.is_valid():
                    s = serializer.save()
                    room_dataa = list(Accommodation.objects.get(id = s['accommodation']).room_set.all())
                    map = []
                    for i in range(len(room_image_data)):
                        map.append({'room':room_dataa[0],"images":room_image_data.pop(0)})
                        if(i%2!=0):
                            room_dataa.pop(0)
                    room_data = [RoomImages(room=row['room'],images=row['images']['image']) for row in map]
                    RoomImages.objects.bulk_create(room_data)
                    return Response({
                        "success":1,
                        "message":"Successfully added hostel"
                    })
                return Response({
                    "success":0,
                    "message":serializer.errors
                })
        except Exception:
            return Response({
                "success":0,
                "message":"Error, Please verify hostel data before sending"
            })
        except:
            return Response({
                "success": 0,
                "message":"Hey there, Please recheck your variables"
            })

class HotelNonTierBasedRoom(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def delete(self,request):
        if request.user.is_authenticated:
            try:
                if 'room_id' not in request.data:
                    return Response({
                        "success":0,
                            "message":"Please send room_id to delete rooms"
                    })
                room = Room.objects.get(id=request.data['room_id'])
                if room.accommodation.vendor.email != request.user.email:
                        return Response({
                            "success":0,
                            "message":"The room doesn't belong to you"
                        })
                if room.accommodation.type!="hotel":
                        return Response({
                            "success":0,
                            "message":"The room isn't a hotel"
                        })
                if room.accommodation.has_tier != False:
                        return Response({
                            "success":0,
                            "message":"The given room has a tier"
                        })
                room_images = RoomImages.objects.get(room=room).delete()
                room.delete()
                return Response({
                    "success":1,
                    "message":"Successfully Deleted"
                })
            except  Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
    def patch(self,request):
        if request.user.is_authenticated:
            try:
                print(request.data)
                if 'room_id' not in request.data:
                        return Response({
                            "success":0,
                            "message":"Please send room_id to add rooms"
                        })
                room = Room.objects.get(id=request.data['room_id'])
                if room.accommodation.vendor.email != request.user.email:
                        return Response({
                            "success":0,
                            "message":"The room doesn't belong to you"
                        })
                if room.accommodation.type!="hotel":
                        return Response({
                            "success":0,
                            "message":"The room isn't a hotel"
                        })
                if room.accommodation.has_tier != False:
                        return Response({
                            "success":0,
                            "message":"The given room has a tier"
                        })
                patchable_fields= [
                            'ac_availability',
                            'seater_beds',
                            'per_day_rent',
                            'fan_availability',
                             'kettle_availability',
                            'coffee_powder_availability',
                            'milk_powder_availability',
                            'tea_powder_availability',
                            'hair_dryer_availability',
                            'tv_availability',
                            'images',
                            'steam_iron_availability',
                            'water_bottle_availability'
                    ]
                updated_fields ={
                    'room':{},
                    'image':{}
                }
                updated_fields["room"]['room_id'] = room.pk

                for fields in patchable_fields:
                    if fields in request.data:
                        if fields == "images":
                            updated_fields["image"]["room"] = room.pk
                            updated_fields["image"]["images"] = request.data[fields]
                        else:
                            updated_fields["room"][fields] = request.data[fields]
                print(updated_fields)
                image = RoomImages.objects.get(room=room)
                print(image.pk)
                room_serializer = RoomAllSerializer(room,data=updated_fields["room"],partial=True)
                room_image_serializer = RoomAllImageSerailizer(image,data=updated_fields["image"],partial=True)
                print(request.data)
                if room_image_serializer.is_valid() and room_serializer.is_valid():
                    room_image_serializer.save()
                    room_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Success"
                    })
                print(room_image_serializer.errors);
                print(room_serializer.errors);

                return Response({
                    "success":0,
                    "message":"Something went wrong"
                })
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
            
    def post(self,request):
        if request.user.is_authenticated:
            try:
                if 'accommodation_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"Please send accommodation_id to add rooms"
                    })
                accommodation = Accommodation.objects.get(id=request.data['accommodation_id'])
                if accommodation.vendor.email != request.user.email:
                        return Response({
                            "success":0,
                            "message":"The accommodation doesn't belong to you"
                        })
                if accommodation.type!="hotel":
                        return Response({
                            "success":0,
                            "message":"The accommodation isn't a hostel"
                        })
                if accommodation.has_tier != False:
                        return Response({
                            "success":0,
                            "message":"The given accommodation has a tier"
                        })
                required_fields= [
                    'ac_availability',
                        'seater_beds',
                        'per_day_rent',
                        'fan_availability',
                         'kettle_availability',
                        'coffee_powder_availability',
                        'milk_powder_availability',
                        'tea_powder_availability',
                        'hair_dryer_availability',
                        'tv_availability',
                        'images',
                        'steam_iron_availability',
                        'water_bottle_availability'
                ]
                mapping = {
                    "room":{},
                    "images":{}
                }
                mapping["room"]["accommodation"] = request.data['accommodation_id']
                for fields in required_fields:
                    if fields not in request.data:
                        return Response({
                            "success":0,
                            "message":f"Hey, there you need to provide {fields}"
                        })
                    if fields in request.data:
                        data = request.data[fields]
                        if data == None or data == "":
                            return Response({
                                "success":0,
                                "message":f"Hey there, the field {fields} cannot be empty"
                            })
                        if fields !='images':
                            mapping["room"][fields] = data
                        if fields == 'images':
                            mapping["images"][fields] = data
                print(mapping)
                serializer = AddNonTierHotelRoomSerializer(data=mapping)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully done"
                    })
                print(serializer.errors)
                return Response({
                    "success":0,
                    "message":'Something went wrong'
                })
            except Accommodation.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The accommodation doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })


            
class HotelNonTierBased(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            if request.user.is_authenticated:
                accommodation = Accommodation.objects.get(id=request.data['accommodation_id'])
                if accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The accommodation doesn't belong to you"
                    })
                if accommodation.type!="hotel":
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a hotel"
                    })
                if accommodation.has_tier != False:
                    return Response({
                        "success":0,
                        "message":"The given accommodation has a tier"
                    })
                accommodation_serialized = AllAccommodationSerializer(accommodation).data
                room = Room.objects.filter(accommodation=accommodation)
                room_serialized = RoomAllSerializer(room,many=True).data
                image = RoomImages.objects.filter(room__in=room)
                image_serialized = RoomAllImageSerailizer(image,many=True).data
                
                return Response({
                    "success":1,
                    "data":{
                        "accommodation":accommodation_serialized,
                        "room":room_serialized,
                        "images":image_serialized
                    }
                })
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"The accommodation doesn't exist"
            })
    def patch(self,request):
        try:
            if request.user.is_authenticated:
                if 'id' not in request.data:
                    return Response({
                        "success":0,
                        "message": "Please provide id in request"
                    })
                accommodation = Accommodation.objects.get(id=request.data['id'])
                if accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The acccommodation doesn't belong to you"
                    })

                # print(accommodation.has_tier);
                if accommodation.has_tier == True:
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a non-tier based"
                    })
                
                hotel_serializer_accommodation = HotelAccommodationSerializer(accommodation,data=request.data,partial=True)
                if hotel_serializer_accommodation.is_valid():
                    hotel_serializer_accommodation.save()
                    print(f"This is serializer {hotel_serializer_accommodation.data}")
                    return Response({
                        "success":1,
                        "message":"Successfully updated accommodation"
                    })
                
                else:
                    return Response({
                        "success":0,
                        "message":hotel_serializer_accommodation.errors
                    })
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"The accommodation doesn't exist"
            })
        except Exception:
            return Response({
                "success":0,
                "message":"Something Wrong"
            })
       
    def post(self,request):
        try:
            if request.user.is_authenticated:
                required_fields = {
                    'accommodation_id',
                    'room[0][ac_availability]',
                    'room[0][seater_beds]',
                    'room[0][per_day_rent]',
                    'room[0][fan_availability]',
                    'room[0][kettle_availability]',
                    'room[0][coffee_powder_availability]',
                    'room[0][milk_powder_availability]',
                    'room[0][tea_powder_availability]',
                    'room[0][hair_dryer_availability]',
                    'room[0][tv_availability]',
                    'room[0][image]'
                }
                for fields in required_fields:
                    if fields not in request.data:
                        return Response({
                            "success":0,
                            "message":f"Please provide {fields} "
                        })
                    if fields in request.data:
                        data = request.data[fields]
                        if data== None or data == "":
                            return Response({
                                "success":0,
                                "message":f"The {fields} cannot be empty or null"
                            })
                accommodation = Accommodation.objects.get(id=request.data['accommodation_id'])
                if accommodation.type !='hotel':
                    return Response({
                        "success":0,
                        "message":"This isn't a hotel"
                    })
                if accommodation.has_tier == True:
                    return Response({
                        "success":0,
                        "message":"This is a tier based accommodation"
                    })
                room_data = {}
                image_data = {}
                mapping = {
                    'room':[],
                    'images':[]
                }
                for data in request.data:
                    if 'room[' in data:
                        field_name = data.split('[')[2].rstrip(']')
                        index = int(data.split('][')[0].split("[")[1])
                        if index not in room_data:
                            room_data[index] = {}
                        field_value = request.data[data]
                        if index in room_data:
                            if field_name == "image":
                                image_data[index]= {'images':request.data[data]} 
                            else:
                                room_data[index][field_name]= field_value
                    # if ''
                # sorted(image_data)
                keys = []

                for key,value in image_data.items():
                    keys.append(key)
                keys.sort()

                for num in keys:
                   mapping["images"].append(image_data[num])
                for key,value in room_data.items():
                    value['accommodation']=accommodation.pk
                    mapping["room"].append(value)

                # print(mapping["images"])
                if(len(mapping["images"]) != len(mapping["room"]) ):
                    return Response({
                        "success":0,
                        "message":"The number of images doesn't match the room count"
                    })
                print(mapping);
                serializer = AddNonTierHotelSerializer(data=mapping)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully added"
                    })
                print(serializer.errors);
            return Response({
                "success":0,
                "message":"Please recheck your values"
            })
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"The accommodation doesn't exit"
            })
        except:
            return Response({
                "success":0,
                "message":"Something went wrong"
            })
class HotelTierBasedAccommodation(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # Add Tier
        try:
            if request.user.is_authenticated:
                print(request.data)
                if 'accommodation' not in request.data:
                    return Response({
                        "success":0,
                        "message": "Please provide id in request"
                    })
                accommodation = Accommodation.objects.get(id=request.data['accommodation'])
                if accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The acccommodation doesn't belong to you"
                    })
                if accommodation.has_tier == False:
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a tier based"
                    })
                hotel_tier_serializer= HotelTierSerializer(
                    data=request.data
                )
                if hotel_tier_serializer.is_valid():
                    hotel_tier_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully Added"
                    })
                return Response({
                    "success":0,
                    "message":hotel_tier_serializer.errors
                })
                # hotel_serializer_accommodation = HotelAccommodationSerializer(accommodation,data=request.data,partial=True)
                # if hotel_serializer_accommodation.is_valid():
                #     hotel_serializer_accommodation.save()
                #     print(f"This is serializer {hotel_serializer_accommodation.data}")
                #     return Response({
                #         "success":1,
                #         "message":"Successfully updated accommodation"
                #     })
                # if 
                # else:
                #     return Response({
                #         "success":0,
                #         "message":hotel_serializer_accommodation.errors
                #     })
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"The accommodation doesn't exist"
            })
        except Exception:
            return Response({
                "success":0,
                "message":"Something Wrong"
            })
    def patch(self,request):
        try:
            if request.user.is_authenticated:
                if 'id' not in request.data:
                    return Response({
                        "success":0,
                        "message": "Please provide id in request"
                    })
                accommodation = Accommodation.objects.get(id=request.data['id'])
                if accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The acccommodation doesn't belong to you"
                    })
                if accommodation.has_tier == False:
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a tier based"
                    })
                hotel_serializer_accommodation = HotelAccommodationSerializer(accommodation,data=request.data,partial=True)
                if hotel_serializer_accommodation.is_valid():
                    hotel_serializer_accommodation.save()
                    print(f"This is serializer {hotel_serializer_accommodation.data}")
                    return Response({
                        "success":1,
                        "message":"Successfully updated accommodation"
                    })
                
                else:
                    return Response({
                        "success":0,
                        "message":hotel_serializer_accommodation.errors
                    })
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"The accommodation doesn't exist"
            })
        except Exception:
            return Response({
                "success":0,
                "message":"Something Wrong"
            })
       
class HotelTierBased(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self,request):
        if request.user.is_authenticated:
            try:
                valid_fields = ['tier_name',
                        'description',
                        'image',]
                hotel_tier = HotelTiers.objects.get(id=request.data['hoteltier_id'])
                if hotel_tier.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success": 0,
                        "message": "This accommodation doesn't belong to you"
                    })
                if not hotel_tier.accommodation.has_tier:
                    return Response({
                        "success": 0,
                        "message": "The accommodation doesn't have a tier"
                    })
                if hotel_tier.accommodation.type!="hotel":
                   return Response({
                       "success":0,
                       "message":"The accommodation isn't a hostel"
                        })
                to_update ={}
                for field in valid_fields:
                    if field in request.data:
                        data = request.data[field]
                        if data == None or data == "":
                            return Response({
                                "success":0,
                                "message":f"The {data} cannot be empty or null"
                            })
                        to_update[field] = data
                hotel_serializer = AllHotelTierSerializer(instance=hotel_tier,data=to_update,partial=True)
                if hotel_serializer.is_valid():
                    hotel_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully Updated"
                    })
                return Response({
                    "success":0,
                    "message":hotel_serializer.errors
                })        
            except HotelTiers.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The hotel tier doesn't exist"
                })
    def delete(self,request):
        if request.user.is_authenticated:
            try:
                hotel_tier = HotelTiers.objects.get(id=request.data['hoteltier_id'])
                if hotel_tier.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success": 0,
                        "message": "This accommodation doesn't belong to you"
                    })
                if not hotel_tier.accommodation.has_tier:
                    return Response({
                        "success": 0,
                        "message": "The accommodation doesn't have a tier"
                    })
                if hotel_tier.accommodation.type!="hotel":
                   return Response({
                       "success":0,
                       "message":"The accommodation isn't a hostel"
                   })
                hotel_tier.delete()
                return Response({
                    "success":1,
                    "message":"Successfully deleted"
                })
            except HotelTiers.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The hotel tier doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something went wrong"
                })
            
    def get(self, request):
         try:
             if request.user.is_authenticated:
                 accommodation = Accommodation.objects.select_related('vendor').get(id=request.data['accommodation_id'])
                 
                 if accommodation.vendor.email != request.user.email:
                     return Response({
                         "success": 0,
                         "message": "This accommodation doesn't belong to you"
                     })
                 if not accommodation.has_tier:
                     return Response({
                         "success": 0,
                         "message": "The accommodation doesn't have a tier"
                     })
                 if accommodation.type!="hotel":
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a hostel"
                    })
                 tier = HotelTiers.objects.filter(accommodation=accommodation)
                 accommodation_serialized = AllAccommodationSerializer(instance=accommodation).data
                 tier_serialized = HotelTierSerializer(tier, many=True).data
                 room = Room.objects.filter(hotel_tier__in=tier).prefetch_related('hotel_tier')
                 room_serializer = RoomAllSerializer(room, many=True)
                 return Response({
                     "success": 1,
                     "data": {
                         "accommodation": accommodation_serialized,
                         "tier": tier_serialized,
                         "room": room_serializer.data
                     }
                 })
         except Accommodation.DoesNotExist:
             return Response({
                 "success": 0,
                 "message": "The accommodation doesn't exist"
             })
         except:
             return Response({
                 "success":0,
                 "message": "Something wen't wrong"
             })
    def post(self,request):
        try:
            if request.user.is_authenticated:
                required_fields = {
                    'accommodation_id',
                    'tier_name',
                    'description',
                    'image',
                    'has_tier',
                    'room[0][ac_availability]',
                    'room[0][water_bottle_availability]',
                    'room[0][steam_iron_availability]',
                    'room[0][per_day_rent]',
                    'room[0][seater_beds]',
                    'room[0][fan_availability]',
                    'room[0][kettle_availability]',
                    'room[0][coffee_powder_availability]',
                    'room[0][milk_powder_availability]',
                    'room[0][tea_powder_availability]',
                    'room[0][hair_dryer_availability]',
                    'room[0][tv_availability]',
                }
                for data in required_fields:
                    if data not in request.data:
                        return Response({
                            "success":0,
                            "message":f"Please provide {data}"
                        })
                    if data in request.data:
                        if request.data[data] == None or request.data[data] == '':
                            return Response({
                                "success":0,
                                "message":f"The {data} cannot be null"
                            })
                # if(acc)
                accommodation = Accommodation.objects.get(id=request.data['accommodation_id'])
                if accommodation.type != 'hotel':
                    return Response({
                        "success":0,
                        "message":"This isn't a hotel"
                    })
                if accommodation.has_tier == False:
                    return Response({
                        "success":0,
                        "message":"This hotel doesn't have a tier"
                    })
                # print(request.user)
                # print(accommodation.vendor)
                if accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"This hotel doesn't belong to you"
                    })
                mapping = {
                    'tier':{
                        'accommodation':request.data.get('accommodation_id'),
                        'tier_name':request.data.get('tier_name'),
                        'description':request.data.get('description'),
                        'image':request.data.get('image')
                    },
                    'rooms':[
                    ]
                }
                fields = {}
                required_fields_rooms = ['ac_availability','water_bottle_availability','steam_iron_availability','per_day_rent','seater_beds','fan_availability','hair_dryer_availability','kettle_availability','coffee_powder_availability','milk_powder_availability','tea_powder_availability','tv_availability']
                for room in request.data:
                    if 'room[' in room:
                        room_index = room.split('[')[1].rstrip(']')
                        name = room.split('[')[2].rstrip(']')
                        if room_index not in fields:
                            fields[room_index]={}
                        fields[room_index][name] = request.data.get(room)
                for field_room in required_fields_rooms:
                    for key,value in fields.items():
                        if field_room not in value:
                            return Response({
                                "success":0,
                                "message":f"{field_room} missing in room {key}"
                            })
                        if field_room in value:
                            data_room = request.data[f'room[{key}][{field_room}]']
                            if data_room == None or data_room == "":
                                return Response({
                                    "success":0,
                                    "message":f"{field_room} cannot have null value in room {key}"
                                }) 
                        if value not in mapping["rooms"]:
                            # print(value)
                            value['accommodation'] = accommodation.pk
                            mapping["rooms"].append(value)
                        # if 
                # print(mapping)
                # mapping["rooms"]["accommodation"]=accommodation.pk
                hotel_serializer = AddHotelTierSerializer(data={'tier':mapping["tier"],'room':mapping["rooms"]})
                if hotel_serializer.is_valid():
                    hotel_serializer.save()
                    return Response({
                        "success":1,
                        "message":hotel_serializer.data
                    })
                return Response({
                        "success":0,
                        "message":hotel_serializer.errors
                    })
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"The accommodation doesn't exist"
            })
        except:
            return Response({
                "success":0,
                "message":"Please check your data before sending :)"
            })
class HotelTierBasedRoom(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        if request.user.is_authenticated:
            try:
                if 'room_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide room id first"
                    })
                room = Room.objects.get(id=request.data['room_id'])
                if room.accommodation.type !='hotel':
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a hotel"
                    })
                if room.accommodation.has_tier == False:
                    return Response({
                        "success":0,
                        "message":"The hotel isn't a tier based"
                    })
                if room.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The accommodation doesn't belong to you :)"
                    })
                room.delete()
                return Response({
                    "success":1,
                    "message":"Successfully deleted"
                })
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something went wrong"
                })
    def post(self,request):
        if request.user.is_authenticated:
            try:
                if 'hoteltier_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide hotel's tier id first"
                    })
                tier = HotelTiers.objects.get(id=request.data['hoteltier_id'])
                if tier.accommodation.type !='hotel':
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a hotel"
                    })
                if tier.accommodation.has_tier == False:
                    return Response({
                        "success":0,
                        "message":"The hotel isn't a tier based"
                    })
                if tier.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The accommodation doesn't belong to you :)"
                    })
                
                valid_fields = ['ac_availability',
                            'water_bottle_availability',
                            'steam_iron_availability',
                            'per_day_rent',
                            'seater_beds',
                            'fan_availability',
                            'kettle_availability',
                            'coffee_powder_availability',
                            'milk_powder_availability',
                            'tea_powder_availability',
                            'hair_dryer_availability',
                            'tv_availability',
                            ]
                for fields in valid_fields:
                    if fields not in request.data:
                        return Response({
                            "success":0,
                            "message":f"Please provide {fields}"
                        })
                    if fields in request.data:
                        data = request.data[fields]
                        if data == None or data == "":
                            return Response({
                                "success":0,
                                "message":f"The field {fields} cannot be null"
                            })
                mapping = {
                    "room":{
                        'ac_availability' : request.data["ac_availability"],
                            'water_bottle_availability' : request.data["water_bottle_availability"],
                            'steam_iron_availability':request.data["steam_iron_availability"],
                            'per_day_rent':request.data["per_day_rent"],
                            'seater_beds':request.data["seater_beds"],
                            'fan_availability':request.data["fan_availability"],
                            'kettle_availability':request.data["kettle_availability"],
                            'coffee_powder_availability':request.data["coffee_powder_availability"],
                            'milk_powder_availability':request.data["milk_powder_availability"],
                            'tea_powder_availability':request.data["tea_powder_availability"],
                            'hair_dryer_availability':request.data["hair_dryer_availability"],
                            'tv_availability':request.data["tv_availability"],
                            'hotel_tier':tier.pk,
                            'accommodation':tier.accommodation.pk
                    }
                }
                room_serializer = RoomAllSerializer(data=mapping["room"])
                if room_serializer.is_valid():
                    room_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully added room"
                    })
                return Response({
                        "success":0,
                        "data":"Something went wrong"
                    }) 
            except HotelTiers.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The hotel tier doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something went wrong"
                })
    
    def patch(self,request):
        if request.user.is_authenticated:
            try:
                print(request.data)
                if 'room_id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"You need to provide room id first"
                    })
                room = Room.objects.get(id=request.data['room_id'])
                if room.accommodation.type !='hotel':
                    return Response({
                        "success":0,
                        "message":"The accommodation isn't a hotel"
                    })
                if room.accommodation.has_tier == False:
                    return Response({
                        "success":0,
                        "message":"The hotel isn't a tier based"
                    })
                if room.accommodation.vendor.email != request.user.email:
                    return Response({
                        "success":0,
                        "message":"The accommodation doesn't belong to you :)"
                    })

                valid_fields = [                    'ac_availability',
                            'water_bottle_availability',
                            'steam_iron_availability',
                            'per_day_rent',
                            'seater_beds',
                            'fan_availability',
                            'kettle_availability',
                            'coffee_powder_availability',
                            'milk_powder_availability',
                            'tea_powder_availability',
                            'hair_dryer_availability',
                            'tv_availability',
                            ]
                patch_fields = {}
                for field in valid_fields:
                    if field in  request.data:
                        data = request.data[field]
                        if data == None or data == "":
                            return Response({
                                "success":0,
                                "message":"The field cannot be null or empty"
                            })
                        patch_fields[field] = data
                # print(patch_fields)
                room_serializer = RoomAllSerializer(instance=room,data = patch_fields,partial=True)
                if room_serializer.is_valid():
                    room_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully updated"
                    })
                return Response({
                    "success":0,
                    "message":"Please recheck your values"
                }) 
            except Room.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The room doesn't exist"
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something went wrong"
                })



class HotelAccommodation(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if request.user.is_authenticated:
            try:
                required_fields = {
                    'name',
                    'image',
                    'city',
                    'address',
                    'longitude',
                    'latitude',
                    'type',
                    'parking_availability',
                    'swimming_pool_availability',
                    'gym_availability',
                    'has_tier',
                }   
                for field in required_fields:
                    if field not in request.data:
                        return Response({
                            "success":0,
                            "message":f"{field} doesn't exist"
                        })
                    if field in request.data:
                        if request.data[field] == None or request.data[field] =="":
                            return Response({
                                "success":0,
                                "message":f"{field} cannot be null"
                            })
                mapping = {
                    'name':request.data.get('name'),
                    'has_tier':request.data.get('has_tier'),
                    'parking_availability':request.data.get('parking_availability'),
                    'gym_availability':request.data.get('gym_availability'),
                    'swimming_pool_availability':request.data.get('swimming_pool_availability'),
                    'latitude':request.data.get('latitude'),
                    'longitude':request.data.get('longitude'),
                    'longitude':request.data.get('type'),
                    'address':request.data.get('address'),
                    'city':request.data.get('city'),
                    'image':request.data.get('image'),
                    'type':request.data.get('type'),
                    'vendor':request.user
                }
                accommodation_serializer = AccommodationAllSerializer(data=mapping)
                if accommodation_serializer.is_valid():
                    accommodation_serializer.save()
                    return Response({
                        "success":1,
                        "message": accommodation_serializer.data
                    })
                else :
                    return Response({
                        "success":0,
                        "message":accommodation_serializer.errors
                    })
            except:
                return Response({
                    "success":0,
                    "message":"Hey there, looks like you are providing invalid fields"
                })
    
