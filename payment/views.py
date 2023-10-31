from payment.models import * 
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *


class GetVendorPaymentData(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        payment_data = Payment.objects.filter(vendor = user)
        serializer = PaymentSerializer(payment_data,many=True)
        if request.user.is_authenticated:
            return Response({
                "success":1,
                "data":serializer.data
            })