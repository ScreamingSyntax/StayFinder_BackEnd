from django.shortcuts import render
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from user.email import generate_otp,send_otp_email
from django.contrib.auth.hashers import make_password
from accomodation.models import Accommodation
from accomodation.serializer import *
from rest_framework import status
from .serializers import *
from customer.models import *
from vendor.models import *
from tier.models import *
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
from datetime import datetime
# Create your views here.


class DashBoardDetails(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request):
        try:
            customers_count = Customer.objects.count()
            vendors_count = VendorUser.objects.count()
            accommodations_count = Accommodation.objects.count()
            tiers_count = Tier.objects.count()
            transactions = TierTransaction.objects.aggregate(
                total_revenue=Sum('paid_amount'),
                avg_transaction=Avg('paid_amount')
            )
            monthly_revenue = TierTransaction.objects.annotate(month=TruncMonth('paid_date')).values('month').annotate(total=Sum('paid_amount')).order_by('-month')[:6]
            active_users_placeholder = {}
            available_accommodations = accommodations_count 
            return Response({
                "success": 1,
                "data": {
                    "customers": customers_count,
                    "vendors": vendors_count,
                    "accommodations": accommodations_count,
                    "tiers": tiers_count,
                    "financial_reports": {
                        "total_revenue": transactions['total_revenue'],
                        "average_transaction_value": transactions['avg_transaction']
                    },
                    "monthly_revenue": list(monthly_revenue),
                }
            })
        except Exception as e:
            return Response({
                "success": 0,
                "message": f"Something went wrong: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ViewUnverifiedAccommodations(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self,request):
        try:
            accommodations = Accommodation.objects.filter(is_verified=False)
            rental = []
            hostel = []
            hotels = []
            hotels_with_tier = []
            for accommodation in accommodations:
                type = accommodation.type
                if type == 'hostel':
                    hostel.append(accommodation)
                elif type == "rent_room":
                    rental.append(accommodation)
                elif type == "hotel" and accommodation.has_tier == False:
                    hotels.append(accommodation)
                elif type == "hotel" and accommodation.has_tier == True:
                    hotels_with_tier.append(accommodation)
            rental_serializer = AccommodationSerializer(rental,many=True)
            hostel_serializer = AccommodationSerializer(hostel,many=True)
            hotel_serializer = AccommodationSerializer(hotels,many=True)
            hotel_with_tier_serializer = AccommodationSerializer(hotels_with_tier,many=True)
            return Response({
                "success":1,
                "data":{
                    "rental":rental_serializer.data,
                    "hostel":hostel_serializer.data,
                    "hotel":hotel_serializer.data,
                    "hotel_tier":hotel_with_tier_serializer.data
                }
            })
        except Exception as e:
            print(e)
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
class AdminLogin(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def post(self,request):
        try:
            if "email" not in request.data:
                return Response({
                    "success":0,
                    "message": "Email is needed to login"
                },
                )
            if "password" not in request.data:
                return Response({
                    "success":0,
                    "message":"Password is needed to login"
                },
                )
            email = request.data['email']
            print(request.data)
            print(email)
            user = BaseUser.objects.get(email=email)
            if(user.user_type == 'vendor'):
                return Response({
                    "success":0,
                    "message":"The Email is used for seller account"
                })
            admin = BaseUser.objects.get(email=email)
            
            if admin.is_accepted == False:
                return Response({
                    "success":0,
                    "message":"Admin Doesn't exist"
                })
            if not admin.check_password(request.data.get('password')):
                return Response({
                    'success': 0,
                    'message': "Wrong Password"
                },
                )
            token, created = Token.objects.get_or_create(user=admin)
            serializer = AdminSerializer(instance=admin)
            return Response({
                "success": 1,
                "token": token.key,
                "data": serializer.data,
                "message":"Successfully Logged In"
            })
        except BaseUser.DoesNotExist:
            return Response({
                "success":0,
                "message":"Admin doesn't exist"
            },
            )
        except:
            return Response({
                "success":0,
                "message":"Customer doesn't exist"
            },
            )


class ViewAccommodationDetail(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self,request):
        try:
            id = self.request.query_params.get('id')
            print(id)
            if not id:
                return Response({
                    'success':0,
                    'message':'Please provide accommodation id'
                })
            accommodation = Accommodation.objects.get(id=id)
            type = accommodation.type
            if type == "rent_room":
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
            if type == "hostel":
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
            has_tier = accommodation.has_tier
            if type == "hotel" and has_tier == False:
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
            if type == "hotel" and has_tier == True:
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
            return Response({
                "success":0,
                "message":"Please recheck the accommodation type"
            })
        
        except Accommodation.DoesNotExist:
            return Response({
                "success":0,
                "message":"Accommodation doesn't exist"
            })
        except Exception as e:
            print(e)
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
            
            