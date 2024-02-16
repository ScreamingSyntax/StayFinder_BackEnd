from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import VendorUser,VendorProfile
from .serializer import VendorSerializer,VendorProfileSerializer
from django.contrib.auth.hashers import make_password
from user.email import generate_otp,send_otp_email
from django.utils import timezone
from django.db import models
from tier.models import TierTransaction,Tier
from user.models import BaseUser
from dateutil.relativedelta import relativedelta 

class ForgotPassword(APIView):
    def post(self,request):
        try:
            print(request.data)
            if 'email' not in request.data:
                return Response({'success':0,'message':'You need to provide email'})
            email = request.data['email']
            user = VendorUser.objects.get(email= email)
            if user.is_accepted == False:
                return Response({'success':0,'message':'The user doesn\'t exist'})
            if user.user_type == 'customer':
                return Response({'success':0,'message':'This email belongs to a seller account'})
            # user=request.user
            if 'otp' not in request.data and 'new_pass' not in request.data:
                otp_bro = generate_otp()
                user.otp = otp_bro
                user.save()
                send_otp_email(email=user.email,otp=otp_bro)
                return Response({'success':1,'message':'The otp has been sent'})
            if 'otp' in request.data and 'new_pass' not in request.data:
                otp = request.data['otp']
                if otp == "" or otp == None:
                    return Response({'success':0,'message':'Otp field cannot be empty'})
                print(otp)
                print(request.data)
                if user.otp != otp:
                    return Response({'success':0,'message':'The otp doesn\'t match'})
                return Response({'success':1,'message':'Otp Verified'})
            if 'otp' in request.data and 'new_pass' in request.data:
                otp = request.data['otp']
                new_pass = request.data['new_pass']
                if otp == "" or otp == None:
                    return Response({'success':0,'message':'Otp field cannot be empty'})
                print(otp)
                print(request.data)
                if user.otp != otp:
                    return Response({'success':0,'message':'The otp doesn\'t match'})
                new_password = make_password(new_pass)
                user.password = new_password
                user.save()
                return Response({'success':1,'message':'Successfully Changed Password'})
        except VendorUser.DoesNotExist:
            return Response({'success':0,'message':'Customer Doesn\'t exist '})
        except Exception as e:
            print(e)
            return Response({'success':0,'message':'Something wen\'t wrong'})


class ResetPassword(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self,request):
        # if 'old_password' not in request.data:
        fields = ['old_pass','new_pass']
        for field in fields:
            if field not in request.data:
                return Response({'success':0,'message':f'Please provide {field} field'})
            if request.data[field] == "" or request.data[field] == None:
                return Response({'success':0,'message':f'The {field} cannot be null'})
        user = VendorUser.objects.get(email=request.user.email)
        # user.check_password
        old_pass = request.data['old_pass']
        if not user.check_password(old_pass):
            return Response({"success":0,"message":"The old password doesn't match"})
        
        password = make_password(request.data['new_pass'])
        user.password = password
        user.save()
        return Response({'success':1,'message':'Password reset successfull'})
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
                vendor = BaseUser.objects.get(email = email)
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
                }
            })            
        else:
            return Response({
                "success": 0,
                "detail": "Invalid Token"
            })

class VendorAcceptData(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if (request.user.is_authenticated):
            if 'id' not in request.data:
                return Response({
                    "success":0,
                    "message":"Please add user id to verify"
                })
            if request.data['id'] == "" or request.data['id'] is str:
                return Response({
                    "success":0,
                    "message":"Please enter valid id"
                })
            vendor_user = VendorUser.objects.get(id = request.data['id'])
            if(vendor_user.vendor_profile.is_verified):
                return Response({
                    "success":0,
                    "message":"The vendor is already verified"
                })
            vendor_user.vendor_profile.is_verified = True
            vendor_user.vendor_profile.is_rejected = False
            vendor_user.date_verified = timezone.now()
            vendor_user.vendor_profile.rejected_message = None
            vendor_user.vendor_profile.is_under_verification_process = False
            vendor_user.save()
            print(timezone.now())
            tier  = TierTransaction(tier=Tier.objects.filter(name="Free Tier").first(),vendor =vendor_user,paid_amount=0,paid_date = timezone.now(),paid_till=timezone.now()+relativedelta(months=1),is_active=True,transaction_id="Free",method_of_payment='Free');
            tier.save()
            return Response({
                    "success":1,
                    "message":"The vendor is successfully verified"
                })
        return Response({
                "success":0,
                "message":"Something wen't wrong"
        })

class VendorRejectData(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if (request.user.is_authenticated):
            if('rejected_message' in request.data):
                vendor_user = VendorUser.objects.get(email = request.user.email)
                if(vendor_user.vendor_profile.is_rejected):
                    return Response({
                        "success":0,
                        "message":"The vendor is already rejected"
                    })
                if(vendor_user.vendor_profile.is_verified):
                     return Response({
                        "success":0,
                        "message":"Cannot reject a verified vendor"
                    })
                vendor_user.vendor_profile.is_rejected = True
                rejected = list(request.data.keys())[0]
                vendor_user.vendor_profile.rejected_message=request.data[rejected]
                vendor_user.vendor_profile.is_under_verification_process = False
                vendor_user.save()
                return Response({
                        "success":1,
                        "message":"The vendor is successfully rejected"
                    })
            else:
                return Response({
                    "success":0,
                    "message":"Please provide a rejected message as well"
                })
        return Response({
                "success":0,
                "message":"Something wen't wrong"
        })
    
class VendorVerificationData(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.is_authenticated:
            print(request.user.email)
            email = request.user.email
            profile = VendorProfile.objects.get(vendor = VendorUser.objects.get(email=email))
            print(profile)
            return Response({
                "success":1,
                "data":{
                    "id":request.user.id,
                    "date_joined":VendorUser.objects.get(email=email).date_joined,
                    "profile_picture":f'/images/{profile.profile_picture}',
                    "citizenship_back":f'/images/{profile.citizenship_back}',
                    "citizenship_front":f'/images/{profile.citizenship_front}',
                    "digital_signature":f'/images/{profile.digital_signature}',
                    "rejected_message":f'{profile.rejected_message}',
                    "address":f'{profile.address}',
                    "is_rejected":f'{profile.is_rejected}',
                    "is_verified":f'{profile.is_verified}',
                    "is_under_verification_process":f'{profile.is_under_verification_process}'
                }
            })
    def patch(self,request):
        if request.user.is_authenticated:
            vendor_user = VendorUser.objects.get(email = request.user.email)
            serializer = VendorProfileSerializer(instance=vendor_user.vendor_profile,data=request.data,partial=True)
            if(serializer.is_valid()):
                if(vendor_user.vendor_profile.is_under_verification_process):
                    return Response ({
                        "success":0,
                        "message":"Your credentials are already for verification"
                    })
                if(vendor_user.vendor_profile.is_rejected):
                    vendor_user.vendor_profile.is_rejected = False
                    vendor_user.vendor_profile.rejected_message = None
                serializer.save()
                return Response({
                    "success":1,
                    "message":"Successfully Send for Verification :)"
                })
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
    
    # def post(self,request