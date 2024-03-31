import json
import django
import os
import base64
from django.core.files.base import ContentFile
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stay_fiinder.settings")
django.setup()
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatMessage
from django.core.serializers.json import DjangoJSONEncoder
from user.models import BaseUser
from user.serializers import BaseUserSerializer
import asyncio
from asgiref.sync import sync_to_async

from notification.send_push import *
class Chating(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = int(self.scope['url_route']['kwargs']['sender_id'])
        self.receiver_id = int(self.scope['url_route']['kwargs']['receiver_id'])
        self.room_channel_name = f"chat_{min(self.sender_id, self.receiver_id)}_{max(self.sender_id, self.receiver_id)}"
        await self.channel_layer.group_add(self.room_channel_name, self.channel_name)
        await self.accept()
        self.message_id_counter = 1  

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_channel_name, self.channel_name)

    @database_sync_to_async
    def save_message_to_database(self, sender, receiver, text=None, image=None):
        message = ChatMessage.objects.create(user=sender, sender=sender, receiver=receiver, message=text)
        if image:
            message.image = image
            message.save()
        return message

    @database_sync_to_async
    def get_user_instance(self, user_id):
        return BaseUser.objects.get(id=user_id)

    async def get_serialized_data(self, user):
        def get_data():
            serializer = BaseUserSerializer(instance=user)
            return serializer.data

        data = await sync_to_async(get_data)()
        return data

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "")
        image_data = text_data_json.get("image")
        sender_id = text_data_json["sender"]
        receiver_id = text_data_json["receiver"]

        sender = await self.get_user_instance(sender_id)
        receiver = await self.get_user_instance(receiver_id)

        image = None
        if image_data:
            image = ContentFile(base64.b64decode(image_data), name='image.jpg')

        await self.save_message_to_database(sender, receiver, message, image)

        sender_data = await self.get_serialized_data(sender)
        receiver_data = await self.get_serialized_data(receiver)
        await sync_to_async(send_push_notification)([receiver], f"New Message from {sender.full_name}", message)
        await self.channel_layer.group_send(self.room_channel_name, {
            "type": 'chat_message',
            "message": message,
            "image": image_data,  
            "sender": sender_data,
            "receiver": receiver_data,
        })

    async def chat_message(self, event):
        event['id'] = self.message_id_counter
        await self.send(text_data=json.dumps({
            'id':event['id'],
            'message': event['message'],
            'image': event['image'],
            'sender': event['sender'],
            'receiver': event['receiver'],
        }))
        self.message_id_counter += 1  


class BinaryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_group_name = f"chat_{min(self.sender_id, self.receiver_id)}_{max(self.sender_id, self.receiver_id)}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_user_instance(self, user_id):
        return BaseUser.objects.get(id=user_id)

    @database_sync_to_async
    def save_binary_data_to_database(self, sender, receiver, image_data):
        return ChatMessage.objects.create(
            user=sender,
            sender=sender,
            receiver=receiver,
            image=image_data,
        )

    async def get_serialized_data(self, user):
        # Wrap the synchronous operations in a function
        def get_data():
            serializer = BaseUserSerializer(instance=user)
            return serializer.data
        
        # Call the synchronous function in an async manner
        data = await sync_to_async(get_data)()
        return data

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        image_data_base64 = text_data_json.get("image")
        if image_data_base64 and image_data_base64.startswith('data:image'):
            header, image_data_base64 = image_data_base64.split(',', 1)
        binary_image_data = base64.b64decode(image_data_base64)
        content_file = ContentFile(binary_image_data, name='image.jpeg')

        sender = await self.get_user_instance(self.sender_id)
        receiver = await self.get_user_instance(self.receiver_id)
        message_instance = await self.save_binary_data_to_database(sender, receiver, content_file)

        sender_data = await self.get_serialized_data(sender)
        receiver_data = await self.get_serialized_data(receiver)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data_json.get("message", ""),
                'sender': sender_data,
                'receiver': receiver_data,
                'image': image_data_base64 
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'receiver': event['receiver'],
            'image': event['image'],  
        }))