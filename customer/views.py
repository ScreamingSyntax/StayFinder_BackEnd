from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from user.email import generate_otp,send_otp_email
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializer import *
from user.serializers import *




class ForgotPassword(APIView):
    def post(self,request):
        try:
            print(request.data)
            if 'email' not in request.data:
                return Response({'success':0,'message':'You need to provide email'})
            email = request.data['email']
            user = Customer.objects.get(email= email)
            if user.is_accepted == False:
                return Response({'success':0,'message':'The user doesn\'t exist'})
            if user.user_type == 'vendor':
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
        except Customer.DoesNotExist:
            return Response({'success':0,'message':'Customer Doesn\'t exist '})
        except Exception as e:
            print(e)
            return Response({'success':0,'message':'Something wen\'t wrong'})
        
class ResetPassword(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self,request):
        fields = ['old_pass','new_pass']
        for field in fields:
            if field not in request.data:
                return Response({'success':0,'message':f'Please provide {field} field'})
            if request.data[field] == "" or request.data[field] == None:
                return Response({'success':0,'message':f'The {field} cannot be null'})
        user = Customer.objects.get(email=request.user.email)
        old_pass = request.data['old_pass']
        new_pass = request.data['new_pass']
        if not user.check_password(old_pass):
            return Response({"success":0,"message":"The old password doesn't match"})
        if(old_pass == new_pass):
            return Response({"success":0,"message":"New password cannot be the same as old "})
        password = make_password(new_pass)
        user.password = password
        user.save()
        return Response({'success':1,'message':'Password reset successfull'})
    
class CustomerView(APIView):
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
            user = BaseUser.objects.get(email = email)
            if(user.user_type == 'vendor'):
                return Response({
                    "success":0,
                    "message":"The Email is used for seller account"
                })
            print("adada")

            customer = Customer.objects.get(email=email)
            print("adada")
            if(customer.is_accepted == False):
                return Response({
                    "success":0,
                    "message":"Customer Doesn't exist"
                })
            if not customer.check_password(request.data.get('password')):
                return Response({
                    'success': 0,
                    'message': "Wrong Password"
                },
                )
            token, created = Token.objects.get_or_create(user=customer)
            print(customer)
            print("adada")

            serializer = CustomerSerializer(
                instance=
                customer)
            return Response({
                "success": 1,
                "token": token.key,
                "user": BaseUserSerializer(user).data,
                "data": serializer.data,
                "message":"Successfully Logged In"
            })
        
        except BaseUser.DoesNotExist:
            return Response({
                "success":0,
                "message":"Customer doesn't exist"
            },
            )
        except Customer.DoesNotExist:
            return Response({
                "success":0,
                "message":"Customer doesn't exist"
            })
        except:
            return Response({
                "success":0,
                "message":"Customer doesn't exist"
            },
            )
    def patch(self,request):
        try:
            customer = Customer.objects.get(id=request.user.id)
            # data = {
            #     "full_name":request.data.get('full_name'),
            #     "image":request.data.get('image')
            # }
            full_name = request.data.get('full_name')
            image = request.data.get('image')
            if not full_name:
                return Response({
                    "success":0,
                    "message":"You need to provide name to update"
                })
            customer.full_name = full_name
            if image:
                customer.image = image
            customer.save()
            return Response({
                "success":1,
                "message":"Customer Details Updated"
            })
        except:
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
    def post(self,request):
            # print()
            print(request.data)
            serializer = CustomerSerializer(data=request.data)
            print(CustomerSerializer)
            required_fields = ['email','password','full_name','image']
            for field in required_fields:
                if(field not in request.data):
                    return Response({
                        "success":0,
                        "message":f"{field} is needed to signup"
                    })
            if serializer.is_valid():
                try: 
                    customer = Customer.objects.get(email=request.data.get('email'))
                    serializer.save()
                    password = make_password(request.data['password'])
                    customer.password = password
                    otp_bro = generate_otp()
                    customer.otp = otp_bro
                    customer.save()
                    print(customer.email)
                    send_otp_email(email=customer.email,otp=otp_bro)
                    return Response({
                        "success":1,
                        "message":"Success Please Verify Otp"
                    });
                except Customer.DoesNotExist as exp:
                    email = request.data['email']
                    serializer.save()
                    customer = Customer.objects.get(email=request.data.get('email'))
                    password = make_password(request.data['password'])
                    customer.password = password
                    otp_bro = generate_otp()
                    customer.otp = otp_bro
                    print("APpe a day")
                    customer.user_type = "customer";
                    customer.save()
                    send_otp_email(email=customer.email,otp=otp_bro)
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
                customer = BaseUser.objects.get(email = email)
                if(customer.is_accepted  == False):
                    if customer.user_type == "vendor":
                        return Response({
                        "success":0,
                        "message":"The email is registered as a seller account"
                    }) 
                if(customer.is_accepted == True):
                    return Response({
                        "success":0,
                        "message":"The Customer account already exists"
                    })
                if(customer.is_accepted == False and otp_exists == True):
                    print(customer.is_accepted)
                    otp = request.data['otp']
                    if(otp == customer.otp):
                        customer.is_accepted = True;
                        customer.save()
                        return Response({
                            'success':1,
                            'message':"Successfully SignedUp In"
                        })
                    return Response({
                        "success":0,
                        "message":"Otp doesn't match"
                    })
                if(customer.is_accepted == False):
                    otp_bro = generate_otp()
                    send_otp_email(email=customer.email,otp=otp_bro)
                    print(request.data)
                    Customer.objects.filter(email=request.data['email']).update(
                    full_name=request.data['full_name'],
                    email=request.data['email'],
                    image=request.data['image'],
                    otp=otp_bro
                    )
                    # customer.save();
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
    