from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from user.email import generate_otp,send_otp_email
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import *
from django.utils import timezone
from booking.models import *
# Create your views here.


class ViewToReviewReviews(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({"success": 0, "message": "User not authorized"})

        bookings = Booking.objects.filter(check_out__lt=timezone.now().date(), user__email=request.user.email)
        reviewed_booking_ids = ReviewModel.objects.filter(booking__isnull=False).values_list('booking_id', flat=True)
        bookings_without_reviews = bookings.exclude(id__in=reviewed_booking_ids)

        # Debugging: Print or log the IDs to ensure the query works as expected
        print(f"Reviewed Booking IDs: {list(reviewed_booking_ids)}")
        print(f"Booking IDs without reviews: {bookings_without_reviews.values_list('id', flat=True)}")

        serializer = FetchBookingSerializer(instance=bookings_without_reviews, many=True)
        return Response({'success': 1, 'data': serializer.data})

class ViewVendorReviews(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self,request):
        if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})
        review = ReviewModel.objects.filter(accommodation__vendor__email == request.user.email).order_by('-added_time')
        review_serializer =FetchReviewSerializer(review,many=False)
        return Response({"success":1,"data":review_serializer.data})

class ViewCustomerReviews(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})
        review = ReviewModel.objects.filter(customer__email = request.user.email,is_deleted=False).order_by('-added_time')
        print(review)
        review_serializer =FetchReviewSerializer(review,many=True)
        return Response({"success":1,"data":review_serializer.data})

class Reviews(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})
        try:
            if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})
            fields = ['title','description','booking']
            for field in fields:
                if field not in request.data:
                    return Response({"success":0,"message":f"Please input {field}"})
                if field in request.data:
                    if request.data[field] == None or request.data[field] == "":
                        return Response({"success":0,"message":f"Please input valid {field}"})
            book = Booking.objects.get(id= request.data['booking'])
            if request.user.email != book.user.email:
                return Response({"success":0,"message":"The booking doesn't exist"})
            if book.check_out > timezone.now().date():
                return Response({"success":0,"message":"You have to wait until you finish your booking period"})
            review = ReviewModel.objects.filter(booking = book)
            print(review)
            if list(review) != []:
                return Response({"success":0,"message":"The review for the accommodaiton already exists"})
            if list(review) != []:
                return Response({"success":0,"message":"You have already added review for this"})
            data = request.data.copy()
            data['customer'] = request.user.id
            data['accommodation']=  book.room.accommodation.id
            serilaizer = ReviewSerializer(data=data)
            print("Accommodation 4")
            if serilaizer.is_valid():
                serilaizer.save()
                return Response({"success":1,"message":"Successfully added review"})
            else:
                print(serilaizer.errors)
            return Response({"success":0,"message":"Error parsing data"})
        except Booking.DoesNotExist:
            return Response({"success":0,"message":"The booking doesn't exist"})
        except Exception as e:
            print(e)
            return Response({"success":0,"message":"Something wen't wrong"})
    def patch(self,request):
        if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})
        try:
            if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})
            # fields = ['id','title','description','image']
            if 'id' not in request.data:
                return Response({"success":0,"message":"Please input review id"})
            id = request.data['id']
            
            review = ReviewModel.objects.get(id=id)
            print("a")
            if review.is_deleted:
                return Response({"success":0,"message":"The accommodation doesn't exist"})
            if review.customer.email != request.user.email:
                return Response({'success':0,'message':'The review doesn\'t belong to you'})
            print("a")
            serializer = ReviewSerializer(instance = review,data=request.data,partial=True)
            print("a")
            if serializer.is_valid():
                serializer.save()
                return Response({"success":1,"message":"Successfully updated"})

            else:
                print(serializer.errors)
                return Response({"success":0,"message":"Please verify your data"})
        except ReviewModel.DoesNotExist:
            return Response({"success":0,"message":"The Review Doesn't exist"})
        except Exception as e:
            print(e)
            return Response({"success":0,"message":"Something wen't wrong"})
    def delete(self,request):
        if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})
        try:
            if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})

            if not request.user.is_authenticated:
                return Response({"success":0,"message":"User not authorized"})
            if 'id' not in request.data:
                return Response({"success":0,"message":"Please input review id"})
            id = request.data['id']
            if id == None or type(id) == str:
                return Response({"success":0,"message":"Please input valid id"})
            review = ReviewModel.objects.get(id=id)
            if review.customer.email != request.user.email:
                return Response({'success':0,'message':'The review doesn\'t belong to you'})
            review.is_deleted = True
            review.save()
            serializer = ReviewSerializer(instance = review)
            return Response({"success":1,"data":serializer.data})
        except ReviewModel.DoesNotExist:
            return Response({"success":0,"message":"The review doesn't exist"})
        except Exception as e:
            print(e)
            return Response({"success":0,"message":"Something wen't wrong"})
        
    def get(self,request):

        try:
            id = request.query_params.get('id', None)
            if id == None:
                    return Response({
                    "success":0,
                    "message":"Please provide accommodation id"
                    })
            review = ReviewModel.objects.filter(is_deleted=False,accommodation__id= id)
            serializer = FetchReviewSerializer(instance = review, many=True)
            return Response({"success":1,"data":serializer.data})
        except:
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })