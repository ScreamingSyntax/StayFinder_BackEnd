from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accomodation.models import *
from .serializers import *
from datetime import datetime
from dateutil.relativedelta import relativedelta 
from accomodation.serializer import *
class ViewParticularBookingDetails(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            param_value = request.query_params.get('id', None)
            if param_value == None:
                    return Response({
                    "success":0,
                    "message":"Please provide product id"
                    })
            booking = Booking.objects.get(id=param_value)
            booking_serializer = FetchBookingSerializer(booking)
            accommodation_type = booking.room.accommodation.type
            if(accommodation_type == "hostel"):
                accommodation_serializer = HostelAccommodationSerializer(  booking.room.accommodation)
                room_serializer = RoomAllSerializer(booking.room)
                room_image = RoomImages.objects.filter(room = booking.room)
                room_image_serializer = RoomImageSerailizer(room_image,many=True)
                return Response({
                    "success":1,
                    "data":{
                        "accommodation":accommodation_serializer.data,
                        "room":room_serializer.data,
                        "images":room_image_serializer.data,
                        "book":booking_serializer.data
                    }
                })
            if(accommodation_type == "rent_room"):
                accommodation_serializer = AccommodationAllSerializer(booking.room.accommodation)
                room_serializer = RoomAllSerializer(booking.room)
                room_image = RoomImages.objects.filter(room= booking.room)
                room_image_serializer = RoomImageSerailizer(room_image,many=True)
                return Response({
                    "success":1,
                    "data":{
                        "accommodation":accommodation_serializer.data,
                        "room":room_serializer.data,
                        "images":room_image_serializer.data,
                        "book":booking_serializer.data
                    }
                })
            if(accommodation_type == "hotel"):
                has_tier = booking.room.accommodation.has_tier
                if has_tier == True:
                    accommodation_serializer = AccommodationAllSerializer(booking.room.accommodation)
                    room_serializer = RoomAllSerializer(booking.room)
                    hotel_tier = HotelTierSerializer(booking.room.hotel_tier)
                    return Response({
                    "success":1,
                    "data":{
                        "accommodation":accommodation_serializer.data,
                        "room":room_serializer.data,
                        "tier":hotel_tier.data,
                        "book":booking_serializer.data
                    }
                })
                if has_tier == False:
                    accommodation_serializer = AccommodationAllSerializer(booking.room.accommodation)
                    room_serializer = RoomAllSerializer(booking.room)
                    room_image = RoomImages.objects.filter(room= booking.room)
                    room_image_serializer = RoomImageSerailizer(room_image,many=True)
                    return Response({
                        "success":1,
                        "data":{
                            "accommodation":accommodation_serializer.data,
                            "room":room_serializer.data,
                            "images":room_image_serializer.data,
                            "book":booking_serializer.data
                        }
                    })
        except Booking.DoesNotExist:
            return Response({
                "success":0,
                "message":"Booking doesn't exist"
            })
        except Exception as e:
            print(e)
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })

class BookingRequestView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        room_id = request.data.get('room_id')
        if not room_id:
            return Response({"success": 0, "message": "Room ID is required."}, status=400)
        try:
            room = Room.objects.get(id=room_id)
            if room.accommodation.vendor == user:
                return Response({"success": 0, "message": "Cannot book your own room."}, status=400)
            if room.accommodation.type not in ['rent_room', 'hostel']:
                return Response({"success": 0, "message": "Booking requests are only for rental rooms and hostels."}, status=400)
            booking_request_data = {
                'room': room.id,
                'user': user.id,
            }
            serializer = BookingRequestSerializer(data=booking_request_data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": 1, "message": "Booking request sent successfully."})
            else:
                return Response({"success": 0, "message": "Invalid data.", "errors": serializer.errors}, status=400)
        except Room.DoesNotExist:
            return Response({"success": 0, "message": "Room not found."}, status=404)

class VerifyBookingRequest(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        book_request_id = request.data.get('book_request_id')
        room_id = request.data.get('room_id')
        status= request.data.get('status')
        if status not in ['accepted','rejected']:
            return Response({"success":0,"message":"Please enter a valid status"})
        if not room_id or not request or not book_request_id:
            return Response({"success":0,"message":"Room ID, book request id  are required"})
        try:
            book = BookingRequest.objects.get(id=book_request_id)
            room = Room.objects.get(id = room_id)
            if book.room != room:
                return Response({"success":0,"message":"The room doesn't belong to this request"})
            print(request.user)
            print(room.accommodation.vendor)
            if room.accommodation.vendor.email != user.email:
                return Response({"success":0,"message":"You can't respond to this request"})
            if book.status == "rejected":
                return Response({"success":0,"message":"The request is already rejected"})
            if book.status == "accepted":
                return Response({"success":0,"message":"The Booking is already accepeted"})
            book.status = status
            book.save()
            return Response({
                "success":1,
                "message":"Successfully Responded To Requests"
            })
        except BookingRequest.DoesNotExist:
            return Response({"success":0,"message":"The request doesn't exist"})
        except Room.DoesNotExist:
            return Response({"success":0,"message":"The room doesn't exist"}) 
        except:
            return Response({"success":0,"message":"Something wen't wrong"})

class BookingView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.user_type == "vendor":
            requests = BookingRequest.objects.filter(room__accommodation__vendor=request.user)
            request_serializer = FetchBookingRequestSerializer(requests,many=True)
            booking =  Booking.objects.filter(room__accommodation__vendor=request.user)
            current_date = datetime.now().date()
            active_bookings = []
            pasts_bookings = []
            
            print(booking)
            for book in booking:
                check_out_date = book.check_out
                if current_date >= check_out_date:
                    pasts_bookings.append(book)
                if current_date < check_out_date:
                    active_bookings.append(book) 
            booking_serializer = FetchBookingSerializer(active_bookings,many=True)
            past_booking_serializer = FetchBookingSerializer(pasts_bookings,many=True)
            return Response({"success":1,"data":{"requests":request_serializer.data,"booking":booking_serializer.data,
                                                 "past_bookings":past_booking_serializer.data
                                                 }})
        if request.user.user_type == "customer":
            requests = BookingRequest.objects.filter(user=request.user)
            request_serializer = FetchBookingRequestSerializer(requests,many=True)
            booking =  Booking.objects.filter(user=request.user)        
            booking_serializer = FetchBookingSerializer(booking,many=True)
            pasts_bookings_serializer  = FetchBookingRequestSerializer(pasts_bookings,many=True)
            return Response({"success":1,"data":{"requests":request_serializer.data,"booking":booking_serializer.data,"pasts_booking":pasts_bookings_serializer.data}})
    def post(self, request):
        user = request.user
        room_id = request.data.get('room_id')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')
        book_request = request.data.get('request_id')
        paid_amount = request.data.get('paid_amount')
        if not room_id or not check_in or not check_out or not paid_amount:
            return Response({"success": 0, "message": "Room ID, check-in, and check-out dates are required."}, status=400)
        try:
            room = Room.objects.get(id=room_id)
            booking_data = {
                'room': room.id,
                'user': user.id,
                'check_in': check_in,
                'check_out': check_out,
                'paid_amount':paid_amount
            }
            if room.accommodation.type in ["hostel","rent_room"]:
                if not book_request:
                    return Response({"success":0,"message":"You need to provide the request id"})
                request = BookingRequest.objects.get(id=book_request)
                if request.room != room:
                    return Response({"success":0,"message":"The room doesn't belong to the request"})
                if request.user.email != user.email:
                    return Response({"success":0,"message":"This request doesn't belong to you"})
                if request.status == "rejected":
                    return Response({"success":0,"message":"Your request was rejected"})
                if request.status == "pending":
                    return Response({"success":0,"message":"The request is pending"})
            if room.room_count <= 0 and room.accommodation.type == "hotel":
                return Response({"success": 0, "message": "No rooms available for booking."}, status=400)
            serializer = BookingSerializer(data=booking_data)
            if serializer.is_valid():
                serializer.save()
                if room.accommodation.type == "hotel":
                    room.room_count -= 1
                    room.save()
                return Response({"success": 1, "message": "Booking confirmed."})
            else:
                return Response({"success": 0, "message": "Invalid data.", "errors": serializer.errors}, status=400)
        except Room.DoesNotExist:
            return Response({"success": 0, "message": "Room not found."}, status=404)
        except BookingRequest.DoesNotExist:
            return Response({"success":0,"message":"The  booking request doesn't exist"})
        except:
            return Response({"success":0,"message":"Something wen't wrong"})