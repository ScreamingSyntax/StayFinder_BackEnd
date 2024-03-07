from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from tier.models import Tier,TierTransaction
from tier.serializers import *
from django.utils import timezone
from dateutil.relativedelta import relativedelta 
from notification.send_push import *
class GetTierInformation(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        tiers = list(Tier.objects.all())
        tiers.sort(key= lambda x: x.pk)
        serializer = TierSerializer(tiers,many=True)
        if request.user.is_authenticated:
            return Response({
                "success":1,
                "data": serializer.data
            })

class GetCurrenTierInformation(APIView):
    authentication_classes=[SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.is_authenticated:
            tiers = TierTransaction.objects.get(vendor=request.user,is_active=True)
            serializer = TransactionTierSerializer(tiers,many=False)
            return Response({
                "success":1,
                "data": serializer.data
            })

class TransactionHistory(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.is_authenticated:
            tiers = TierTransaction.objects.filter(vendor=request.user)
            serializer = PaymentSerializer(tiers,many=True)
            return Response({
                "success":1,
                "data":serializer.data
            })
        
class RenewTier(APIView):
    authentication_classes=[SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if request.user.is_authenticated:
            print(request.user)
            # if 
            request.data['vendor']=request.user
            request.data['is_active']=True
            request.data['paid_date']=timezone.now()
            print(request.data)
            requested_fileds  = ['tier','method_of_payment','transaction_id','paid_amount','paid_till']
            for data in requested_fileds:
                if(data not in request.data):
                    return Response({
                        "success":0,
                        "message":f"Please provide {data} field"
                    })
            print(request.data)
            try:
                serializer = TransactionTierSerializer(data=request.data)
                if(serializer.is_valid()):
                    print(serializer.validated_data['tier'])
                    print();
                    if(serializer.validated_data['tier']== Tier.objects.get(name="Free Tier").pk):
                        return Response({
                            "success":0,
                            "message":"Cannot purchase free tier"
                        })
                    TierTransaction.objects.filter(vendor=request.user).update(is_active=False)
                    serializer.save();
                    return Response({
                        "success":0,
                        "message":"Successfully renewed tier"
                    });

                print(serializer.errors)
                return Response({
                        "success":0,
                        "message":""
                    });
            except Exception as e:
                print(e)
                return Response({
                    'success':0,
                    'message':'Invalid Credentials'
                })