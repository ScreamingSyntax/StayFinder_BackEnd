from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from tier.models import Tier,TierTransaction
from accomodation.serializer import *
from collections import namedtuple
import json
Rent = namedtuple('Rent',('accommodation','room_serializer'))

class RentalRoom(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if request.user.is_authenticated:
            accommodation  = Accommodation.objects.get(id=request.data['accommodation'],vendor=request.user)
            room_serializer= Room.objects.get(accommodation=accommodation)
            rent = Rent(
                accommodation=accommodation,
                room_serializer=room_serializer
            )
            serializer = RentRoomSerialzer(rent)
            print(serializer.data)
            return Response({
                "success":0,
                "data":{
                    'accommodation':serializer.data['accommodation'],
                    'room':serializer.data['room_serializer']
                }
            })
        
    def post(self, request):
        if request.user.is_authenticated:
            print(request.data['accommodation[image]'])
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
                     "image":request.data.get('accommodation[image]')
                 },
                 "room": {
                     "fan_availability": request.data.get('room[fan_availability]'),
                     "bed_availability": request.data.get('room[bed_availability]'),
                     "sofa_availability": request.data.get('room[sofa_availability]'),
                     "mat_availability": request.data.get('room[mat_availability]'),
                     "carpet_availability": request.data.get('room[carpet_availability]'),
                     "washroom_status": request.data.get('room[washroom_status]'),
                       "dustbin_availability": request.data.get('room[dustbin_availability]'),
                     }
            }
            print(mapping)
            mapping['accommodation']['vendor'] = request.user
            mapping['room']['accommodation'] = mapping['accommodation']
            rent = Rent(
                accommodation= mapping['accommodation'],
                room_serializer=mapping['room']
            )
            for room in room_fields:
                if room not in list(rent.room_serializer):
                    return Response({
                        'success':0,
                        'message':f"Please provide {room} field"
                    })
            serializer = RentRoomSerialzer(data={'accommodation': rent.accommodation, 'room_serializer': rent.room_serializer})
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
