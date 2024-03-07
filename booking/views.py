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
from .models import *
from django.db.models import Sum, Avg, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Cast, TruncDay, TruncWeek, TruncMonth, TruncYear
from django.db.models.functions import Cast
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from notification.models import Notification
from notification.send_push import *

class RevenueView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        period = request.query_params.get('period', None)
        print(f"The period is {period}");
        bookings = Booking.objects.annotate(
            paid_amount_decimal=ExpressionWrapper(
                Cast('paid_amount', DecimalField(max_digits=10, decimal_places=2)),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        ).filter(room__accommodation__vendor__email = request.user.email)
        total_revenue = bookings.aggregate(Sum('paid_amount_decimal'))['paid_amount_decimal__sum'] or 0
        average_revenue_per_booking = bookings.aggregate(Avg('paid_amount_decimal'))['paid_amount_decimal__avg'] or 0
        revenue_by_accommodation = bookings.values('room__accommodation__name').annotate(
            total_revenue=Sum('paid_amount_decimal')
        ).order_by('room__accommodation')
        response_data = {
            'total_revenue': total_revenue,
            'average_revenue_per_booking': average_revenue_per_booking,
            'revenue_by_accommodation': list(revenue_by_accommodation),
        }
        if period:
            trunc_functions = {
                'daily': TruncDay,
                'weekly': TruncWeek,
                'monthly': TruncMonth,
                'yearly': TruncYear,
            }
            if period in trunc_functions:
                bookings_with_period = bookings.annotate(
                    period=trunc_functions[period]('booked_on')
                )
                revenue_by_period = bookings_with_period.values('period').annotate(
                    total_revenue=Sum('paid_amount_decimal'),
                    average_revenue=Avg('paid_amount_decimal')
                ).order_by('period')
                response_data['revenue_by_period'] = list(revenue_by_period)
            else:
                response_data['error'] = 'Invalid period specified'
                return Response({
                    'success':0,
                    'message':"Invalid Period specified"
                })
        return Response({
                    "success":1,
                    "data":response_data
                })
    
class WishListView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            wishlist = WhishList.objects.filter(user = request.user).exclude(is_deleted=True).order_by('-id')
            wishlist_serializer = WishListSerializer(wishlist,many=True)
            return Response({"success":1,"data":wishlist_serializer.data})
        except WhishList.DoesNotExist:
            return Response({"success":0,"message":"The accommodation doesn't exist"})
        except:
            return Response({"success":0,"message":"Something wen't wrong"})
    def delete(self,request):
        try:
            print(request.data)
            if 'id' not in request.data:
                return Response({"success":0,"message":"Please add wishlist id to delete"})
            accommodation = Accommodation.objects.get(id=request.data["id"])
            wishlist = WhishList.objects.filter(accommodation=accommodation).update(is_deleted=True)
            return Response({"success":1,"message":"Successfuly Removed from wishlist"})
        except Accommodation.DoesNotExist:
            return Response({"success":0,"message":"The accommodation doesn't exist"})
        except WhishList.DoesNotExist:
            return Response({"success":0,"message":"The accommodation doesn't exist"})
        except Exception as e:
            print(e)
            return Response({"success":0,"message":"Something wen't wrong"})
    def post(self,request):
        try:
            if 'id' not in request.data:
                return Response({"success":0,"message":"Please add accommodation id"})
            accommodation = Accommodation.objects.get(id=request.data['id'])
            wishlist = list( WhishList.objects.filter(accommodation = accommodation).exclude(is_deleted = True))
            if wishlist != []:
                return Response({"success": 0,"message":"The accommodation is already added to wishlist"})
            print(f"This is wishlist {wishlist}")
            wishlist = WhishList.objects.create(accommodation = accommodation, user = request.user)
            wishlist.save()
            return Response({"success":1,"message":"Successfully added to wishlist"})
        except Accommodation.DoesNotExist:
            return Response({"success":0,"message":"The accommodation doesn't exist"})
        except  Exception as e:
            print(e )
            return Response({"success":0,"message":"Something wen't wrong"})

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
                booking_request = serializer.save()
                channel_layer = get_channel_layer()
                group_name = f"notifications_vendor_{booking_request.room.accommodation.vendor.id}"
                if group_name:
                    message = {
                        'type': 'broadcast_notification',
                        'message': {
                            'description':f"Your accommodation has a booking request by {booking_request.user.full_name}",
                            'notification_type': 'info',
                        },
                        'user_id':booking_request.room.accommodation.vendor.id
                    }
                async_to_sync(channel_layer.group_send)(group_name, message)
                notification = Notification.objects.create(vendor = booking_request.room.accommodation.vendor,description =f"Your accommodation has a booking request by {booking_request.user.full_name}",notification_type='warning' )
                notification.save()
                user = BaseUser.objects.filter(email = booking_request.room.accommodation.vendor.email)
                send_push_notification(user,"Booking Request",notification.description)
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
        notification_type=""
        if status not in ['accepted','rejected']:
            return Response({"success":0,"message":"Please enter a valid status"})
        if not room_id or not request or not book_request_id:
            return Response({"success":0,"message":"Room ID, book request id  are required"})
        if status == 'accepted':
            notification_type = "success"
        if status == 'rejected':
            notification_type = "failure"
        try:
            book = BookingRequest.objects.get(id=book_request_id)
            room = Room.objects.get(id = room_id)
            if book.room != room:
                return Response({"success":0,"message":"The room doesn't belong to this request"})
            # print(request.user)
            # print(room.accommodation.vendor)
            # base = BaseUser.objects.filter(email = room.accommodation.vendor.email)
            if room.accommodation.vendor.email != user.email:
                return Response({"success":0,"message":"You can't respond to this request"})
            if book.status == "rejected":
                return Response({"success":0,"message":"The request is already rejected"})
            if book.status == "accepted":
                return Response({"success":0,"message":"The Booking is already accepeted"})
            book.status = status
            book.save() 
            channel_layer = get_channel_layer()
            print(f"This is notification type  {notification_type}")
            notification = Notification.objects.create(customer = book.user,description=f'Your booking request has been {status}',notification_type=notification_type)
            print("dad")
            base = BaseUser.objects.filter(email=book.user.email)
            print("daa")
            
            send_push_notification(base,"Booking Request",notification.description)
            print("dadadada")
            target = notification.target
            group_name = f"notifications_customer_{notification.customer.id}"
            if group_name:
                message = {
                    'type': 'broadcast_notification',
                    'message': {
                        'description': notification.description,
                        'notification_type': notification.notification_type,
                    },
                    'user_id': book.user.id
                }
                async_to_sync(channel_layer.group_send)(group_name, message)
            notification.save()
            print("dada")
            return Response({
                "success":1,
                "message":"Successfully Responded To Requests"
            })
        except BookingRequest.DoesNotExist:
            return Response({"success":0,"message":"The request doesn't exist"})
        except Room.DoesNotExist:
            return Response({"success":0,"message":"The room doesn't exist"}) 
        except Exception as e:
            print(e)
            return Response({"success":0,"message":"Something wen't wrong"})

class ViewBookingHistory(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        bookings = Booking.objects.filter(user=user).order_by('-check_out')
        booking_serializer = FetchBookingSerializer(bookings,many=True)
        return Response({"success":1,"data":booking_serializer.data})
    
class ViewBookingRequestHistory(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        booking_requests = BookingRequest.objects.filter(user=user).order_by('-requested_on')
        request_serializer = FetchBookingRequestSerializer(booking_requests,many=True)
        return Response({"success":1,"data":request_serializer.data})
    
class BookingView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if request.user.user_type == "vendor":
            requests = BookingRequest.objects.filter(room__accommodation__vendor=request.user).order_by('-requested_on')
            request_serializer = FetchBookingRequestSerializer(requests,many=True)
            booking =  Booking.objects.filter(room__accommodation__vendor=request.user).order_by('-check_out')
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
            return Response({"success":1,"data":{"requests":request_serializer.data,"booking":booking_serializer.data, "past_bookings":past_booking_serializer.data}})
        
        if request.user.user_type == "customer":
            requests = BookingRequest.objects.filter(user=request.user,is_used = False,).exclude(status = "rejected").order_by('-requested_on')
            request_serializer = FetchBookingRequestSerializer(requests,many=True)
            booking =  Booking.objects.filter(user=request.user).order_by('-check_out')   
            booking_serializer = FetchBookingSerializer(booking,many=True)
            current_date = datetime.now().date()
            active_bookings = []
            print(booking)
            for book in booking:
                check_out_date = book.check_out
                print(check_out_date)
                print(current_date)
                if current_date < check_out_date:
                    active_bookings.append(book) 
            active_bookings_serializer  = FetchBookingSerializer(active_bookings,many=True)
            return Response({"success":1,"data":{"requests":request_serializer.data,"booking":active_bookings_serializer.data}})
        
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
                request.is_used = True
                request.save()
            if room.room_count <= 0 and room.accommodation.type == "hotel":
                return Response({"success": 0, "message": "No rooms available for booking."}, status=400)
            
            serializer = BookingSerializer(data=booking_data)
            
            if serializer.is_valid():
                book = serializer.save()  
                channel_layer = get_channel_layer()
                group_name = f"notifications_vendor_{book.room.accommodation.vendor.id}"
                if group_name:
                    message = {
                        'type': 'broadcast_notification',
                        'message': {
                            'description': f"Your accommodation has been book by {book.user.full_name}",
                            'notification_type': 'info',
                        },
                         'user_id':book.room.accommodation.vendor.id
                    }
                async_to_sync(channel_layer.group_send)(group_name, message)
                notification = Notification.objects.create(vendor = book.room.accommodation.vendor,description =f"Your accommodation has been book by {book.user.full_name}",notification_type='info' )
                notification.save()
                base = BaseUser.objects.filter(email=book.room.accommodation.vendor.email)
                send_push_notification(base,"Book",notification.description)
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
        except Exception as e:
            print(e)
            return Response({"success":0,"message":"Something wen't wrong"})