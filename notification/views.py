from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from customer.models import *
from vendor.models import *
from user.models import BaseUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# from .send_push import send_push_notificati
from .send_push import *

class RegisterDevice(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        try:
            if not request.user.is_authenticated:
                return Response({'success':0,'message':'Token missing'})
            notification = NotificationDevice.objects.filter(user=request.user)
            notification_serializer = NotificationDeviceSerializer(notification,many=True)
            return Response({'success':1,'data':notification_serializer.data})
        except:
            return Response({'success':0,'message':'Something wen\'t wrong'})
    def delete(self,request):
        try:
            if not request.user.is_authenticated:
                return Response({'success':0,'message':'Token missing'})
            if 'device_id' not in request.data:
                return Response({'success':0,'message':'Device Id Missing'})
            device_id = request.data['device_id']
            if device_id == "" or device_id == None:
                return Response({'success':0,'message':'Device id cannot be null or empty'})
            notification_device = NotificationDevice.objects.get(device_id=device_id)
            if(notification_device.user != request.user):
                return Response({'success':0,'message':'You aren\'t allowed to perform this action'})
            notification_device.delete()
            return Response({'success':1,'message':'Successfully Removed Access'})
        except NotificationDevice:
            return Response({'success':0,'message':'Device doesn\'t exist'})
    def post(self,request):
        try:
            print(request.data)
            if not request.user.is_authenticated:
                return Response({'success':0,'message':'The user isn\'t authenticated '})
            if 'device_id' not in request.data:
                return Response({'success':0,'message':'Please provide device id'})
            user = request.user
            notifications = NotificationDevice.objects.filter(user =user, device_id = request.data['device_id'])

            if list(notifications) != []:
                return Response({'success':1,'message':'The device is already registered'})
            notifications_user = NotificationDevice.objects.filter(device_id = request.data['device_id'])
            if list(notifications_user) !=[]:

                notifications_user.update(user= user)
                return Response({'success':1,'message':'The device id has been registered'})
            # device_id = ""
            if 'device_model' in request.data:
                device_model_name = request.data['device_model']
                device = NotificationDevice.objects.create(user = user, device_id = request.data['device_id'],device_model=device_model_name)
                device.save()
            else:
                device_model = NotificationDevice.objects.create(user = user, device_id = request.data['device_id'])
                device_model.save()
            return Response({'success':1,'message':'The device id has been registered'})
        except Exception as e:
            print(e) 
            return Response({'success':0,'message':'Something wen\'t wrong'})

class NotificationAPIView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def notify_websocket_clients(self, notification):
            channel_layer = get_channel_layer()
            group_name = 'notifications_group'  # Example group name, adjust as needed
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'refresh_notifications',  # Corresponds to the method in your consumer
                    'message': notification
                }
        )
    def post(self, request, *args, **kwargs):
        fields = ['description']
        for field in fields:
            if field not in request.data:
                return Response({'success': 0, 'message': f'The field {field} should be provided'})
            data = request.data[field]
            if data is None or data == "":
                return Response({'success': 0, 'message': f'The field {field} cannot be null'})
        
        request.data['notification_type'] = request.data.get('notification_type', 'info')
        
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()            
            channel_layer = get_channel_layer()
            target = notification.target
            group_names_and_ids = [] 
            if target == "all":
                users = BaseUser.objects.all()
                print("ada")
                send_push_notification(users,'Announcement',request.data['description'])
                group_names_and_ids.append(("notifications_general", None))  
            elif target == "customer":
                customer_ids = [customer.id for customer in Customer.objects.all()]
                customers = BaseUser.objects.filter(user_type='customer')
                send_push_notification(customers,'Announcement',request.data['description'])
                group_names_and_ids.extend([(f"notifications_customer_{id}", id) for id in customer_ids])
            elif target == "vendor":
                vendor_ids = [vendor.id for vendor in VendorUser.objects.all()]
                vendors = BaseUser.objects.filter(user_type='vendor')
                send_push_notification(vendors,'Announcement',request.data['description'])
                group_names_and_ids.extend([(f"notifications_vendor_{id}", id) for id in vendor_ids])
            for group_name, user_id in group_names_and_ids:
                message = {
                    'type': 'broadcast_notification',
                    'message': {
                        'description': notification.description,
                        'notification_type': notification.notification_type,
                    },
                    'user_id': user_id 
                }
                async_to_sync(channel_layer.group_send)(group_name, message)
            return Response({'success': 1, 'message': 'Successfully announced'})
        else:
            return Response({'success': 0, 'message': serializer.errors})
    def get(self, request):
        if request.user.is_authenticated:
            try:
                user = BaseUser.objects.get(email=request.user.email)
                is_customer = user.user_type == 'customer'
                is_vendor = user.user_type == 'vendor'
                if is_customer:
                    notifications = Notification.objects.filter(Q(customer__email=user.email) | Q(target='all') | Q(target='customer')).exclude(target='vendor').order_by('-added_date')
                elif is_vendor:
                    notifications = Notification.objects.filter(Q(vendor__email=user.email) | Q(target='all') | Q(target='vendor')).exclude(target='customer').order_by('-added_date')
                else:
                    notifications = Notification.objects.none() 
                serializer = NotificationSerializer(notifications, many=True)
                return Response(serializer.data)
            except BaseUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        else:
            notifications = Notification.objects.filter(target='all')
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
