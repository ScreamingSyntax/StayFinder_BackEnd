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

from rest_framework import status
from .serializers import *
# Create your views here.

class AdminLogin(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self,request):
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
            user = BaseUser.objects.get(email = email)
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