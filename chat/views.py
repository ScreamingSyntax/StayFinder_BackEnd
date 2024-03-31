from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from .models import *
from rest_framework import generics,status
from .serializers import *
from vendor.models import *
from customer.models import *
from django.db.models import Q
from django.db.models import Case, When, Value, CharField, F


class GetSearchMessages(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def post(self,request):
        sender_id = self.request.query_params.get('sender_id')
        try:
            messages = ChatMessage.objects.filter(reciever__id = sender_id)
            messages_serializer = MessageSerializer(messages)
            if messages_serializer.is_valid():
                return Response({
                    "success":1,
                    "data":messages_serializer.data
                })
            return Response({
                "success":0,
                "message":"Error parsing data"
            })
        except:
            return Response({
                "success":0,
                "messages":"Err"
            })

class GetMainScreenMessages(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self, request):
        sender_id = self.request.query_params.get('sender_id')
        try:
            if not request.user.is_authenticated:
                return Response({'success': 0, 'message': 'Invalid Token'})
            messages = ChatMessage.objects.annotate(
                conversation_id=Case(
                    When(sender_id=sender_id, then=F('receiver_id')),
                    When(receiver_id=sender_id, then=F('sender_id')),
                    output_field=CharField(),
                )
            ).filter(
                Q(sender_id=sender_id) | Q(receiver_id=sender_id)
            ).order_by('conversation_id', '-date').distinct('conversation_id')
            serializer = SendMessageSerializer(messages, many=True)
            return Response({
                "success": 1,
                "data": {
                    'messages':serializer.data
                }
            })
        except Exception as e:
            return Response({
                "success": 0,
                "message": f"Something went wrong: {str(e)}"
            })

class SearchMessages(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def post(self,request):
        try:
            if not request.user.is_authenticated:

                return Response({
                    "success":0,
                    "message":"Invalid Token or Missing"
                })
            sender_id = self.request.query_params.get('sender_id')
            if not sender_id:
                return Response({
                    "success":0,
                    "message":'You need to provide sender id'
                })
            if 'value' not in request.data:
                return Response({
                    "success":0,
                    "message":"No search text provided"
                })
            value = request.data['value']
            if value == None:
                return Response({
                    "success":0,
                    "message": "Search Value cannot be null"
                })
            if sender_id == "" or sender_id == None:
                return Response({
                    "success":0,
                    "message":"Please provider sender id"
                })
            messages = ChatMessage.objects.annotate(
                conversation_id=Case(
                    When(sender_id=sender_id, then=F('receiver_id')),
                    When(receiver_id=sender_id, then=F('sender_id')),
                    output_field=CharField(),
                )
            ).filter(
                Q(sender_id=sender_id) | Q(receiver_id=sender_id)
            ).order_by('conversation_id', '-date').distinct('conversation_id').filter(
                receiver__full_name__contains = value
            )
            return Response({
                'success':1,
                'data':
                {
                     "messages":  SendMessageSerializer(messages,many=True).data
                }
              
            })
        except:
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
class GetMessages(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self,request):
        try:
            if not request.user.is_authenticated:
                return Response({'success': 0, 'message': 'Invalid Token'})
            sender_id = self.request.query_params.get('sender_id')
            receiver_id = self.request.query_params.get('receiver_id')
            messages = ChatMessage.objects.filter(
                sender__in=[sender_id, receiver_id],
                receiver__in=[sender_id, receiver_id]
            ).order_by('date')
            serializer_class = SendMessageSerializer(messages,many=True)
            images = ""
            baseuser = BaseUser.objects.get(id=receiver_id)
            print(baseuser.user_type)
            if baseuser.user_type == "vendor":
                    vendor = VendorProfile.objects.get(vendor__email=baseuser.email)
                    print(vendor)
                    images = vendor.profile_picture
            if baseuser.user_type  == "customer":
                    customer = Customer.objects.get(email = baseuser.email)
                    images = customer.image
            link = f"/images/{(str(images))}"
            print(link)
            return Response({
                'success':1,
                'data':{
                    'messages':serializer_class.data,
                    'reciever_image':link
                }
            })
        except:
            return Response({
                'success':0,
                'message':'Something wen\'t wrong'
            })
    def post(self,request):
        try:
            if not request.user.is_authenticated:
                return Response({'success': 0, 'message': 'Invalid Token'})
            sender_id = self.request.query_params.get('sender_id')
            receiver_id = self.request.query_params.get('receiver_id')
            ChatMessage.objects.filter(
                sender__in=[sender_id, receiver_id],
                receiver__in=[sender_id, receiver_id]
            ).update(is_read=True)
            return Response({
                'success':1,
                'message':"Successfully Seen"
            })
        except:
            return Response({
                'success':0,
                'message':'Something wen\'t wrong' 
            })