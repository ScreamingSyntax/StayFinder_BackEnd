from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import VendorUser
from .serializer import VendorSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from user.email import generate_otp,send_otp_email
from django.db import models

class LoginView(APIView):
    def post(self, request):
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
            user = VendorUser.objects.get(email=request.data.get('email'))

            if(user.is_accepted == False):
                return Response({
                    "success":0,
                    "message":"Vendor Doesn't exist"
                })
            if not user.check_password(request.data.get('password')):
                return Response({
                    'success': 0,
                    'message': "Wrong Password"
                },
                )
            token, created = Token.objects.get_or_create(user=user)
            serializer = VendorSerializer(instance=user)
            return Response({
                "success": 1,
                "token": token.key,
                "user": serializer.data,
                "message":"Successfully Logged In"
            })
        except:
            return Response({
                "success":0,
                "message":"Vendor doesn't exist"
            },
            )

class SignUpView(APIView):
    def post(self,request):
        # try:
            serializer = VendorSerializer(data=request.data)
            required_fields = ['email','password','full_name','phone_number','user_type']
            for field in required_fields:
                if(field not in request.data):
                    return Response({
                        "success":0,
                        "message":f"{field} is needed to signup"
                    })
            if serializer.is_valid():
                try: 
                    vendor = VendorUser.objects.get(email=request.data.get('email'))
                    serializer.save()
                    password = make_password(request.data['password'])
                    vendor.password = password
                    otp_bro = generate_otp()
                    vendor.otp = otp_bro
                    vendor.save()
                    send_otp_email(email=vendor.email,otp=otp_bro)
                    return Response({
                        "success":1,
                        "message":"Success Please Verify Otp"
                    });
                except VendorUser.DoesNotExist as exp:
                    email = request.data['email']
                    serializer.save()
                    vendor = VendorUser.objects.get(email=request.data.get('email'))
                    password = make_password(request.data['password'])
                    vendor.password = password
                    otp_bro = generate_otp()
                    vendor.otp = otp_bro
                    vendor.save()
                    send_otp_email(email=vendor.email,otp=otp_bro)
                    return Response({
                        "success":1,
                        "message":"Success Please Verify Otp"
                    });            
            print(serializer._errors['email'][0].title())
            if(serializer._errors['email'][0].title() == "Base User With This Email Already Exists."):
                email = request.data['email']
                otp_exists = False
                if 'otp' in request.data:
                    otp_exists = True
                vendor = VendorUser.objects.get(email = email)
                if(vendor.is_accepted == True):
                    return Response({
                        "success":0,
                        "message":"The vendor account already exists"
                    })
                if(vendor.is_accepted == False and otp_exists == True):
                    print(vendor.is_accepted)
                    otp = request.data['otp']
                    if(otp == vendor.otp):
                        vendor.is_accepted = True;
                        vendor.save()
                        return Response({
                            'success':1,
                            'message':"Successfully SignedUp In"
                        })
                    return Response({
                        "success":0,
                        "message":"Otp doesn't match"
                    })
                if(vendor.is_accepted == False):
                    otp_bro = generate_otp()
                    send_otp_email(email=vendor.email,otp=otp_bro)
                    print(request.data)
                    VendorUser.objects.filter(email=request.data['email']).update(
                    full_name=request.data['full_name'],
                    phone_number=request.data['phone_number'],
                    user_type=request.data['user_type'],
                    otp=otp_bro
                    )
                    # vendor.save();
                    return Response({
                        "success":1,
                        "message":"Success, Now verify OTP"
                    })  
            return Response(
                {
                    "success":0,
                    "message":list(serializer.errors.values())[0][0]
                }
                ,status=status.HTTP_400_BAD_REQUEST)
        # except Exception:
        #     print("niga")

class GetVendorData(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            print("Authenticated")
            return Response({
                "success":1,
                "data":{
                    "id":request.user.id,
                    "email":f"{request.user.email}",
                    "fullName":f"{request.user.full_name}",
                    "phoneNumber":f"{request.user.phone_number}",
                    "isVerified":VendorUser.objects.get(email=request.user.email).is_verified
                }
            })            
        else:
            return Response({
                "success": 0,
                "detail": "Invalid Token"
            })

