from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from user.models import BaseUser
from notification.models import Notification
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from channels.db import database_sync_to_async
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token_key = self.scope['query_string'].decode('utf-8').split('=')[1]
        if token_key:
            user = await self.authenticate_user(token_key)
            if user:
                self.user = user
                await self.accept()
                if user.user_type == 'customer':
                    group_name = f"notifications_customer_{user.id}"
                elif user.user_type == 'vendor':
                    group_name = f"notifications_vendor_{user.id}"
                else:
                    group_name = "notifications_general"  
                
                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
                
                if self.user.is_authenticated:
                    await self.send_notifications()
                else:
                    await self.close()
            else:
                await self.close()
        else:
            await self.close()


    async def broadcast_notification(self, event):
        user_id = event.get('user_id')
        if user_id:
            user = await database_sync_to_async(BaseUser.objects.get)(id=user_id)
            if user:
                notifications = await self._get_user_notifications(user)
                notifications_data = await self._serialize_notifications(notifications)
                await self.send(text_data=json.dumps(notifications_data))
            else:
                print("User not found.")  
        else:
            print("User ID not provided in event.")  

    async def authenticate_user(self, token_key):
        user = await database_sync_to_async(self._get_user_from_drf_token)(token_key)
        return user


    @staticmethod
    def _get_user_from_drf_token(token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    async def send_notifications(self):
        notifications = await self._get_user_notifications(self.user)
        notifications_data = await self._serialize_notifications(notifications)
        await self.send(text_data=json.dumps(notifications_data))


    @database_sync_to_async
    def _get_user_notifications(self, user):
        if user.user_type == 'customer':
            notifications = Notification.objects.filter(Q(customer__email=user.email) | Q(target='all') | Q(target='customer')).exclude(target='vendor')
        elif user.user_type == 'vendor':
            notifications = Notification.objects.filter(Q(vendor__email=user.email) | Q(target='all') | Q(target='vendor')).exclude(target='customer')
        else:
            notifications = Notification.objects.none()  
        return notifications

    @database_sync_to_async
    def _serialize_notifications(self, notifications):
        serializer = NotificationSerializer(notifications, many=True)
        return serializer.data