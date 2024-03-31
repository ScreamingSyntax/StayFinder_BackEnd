# myproject/routing.py
from django.urls import path
# from order.consumers import *
from notification.consumers import NotificationConsumer
from chat.consumers import Chating,BinaryConsumer
websocket_urlpatterns = [
    path('ws/notification/', NotificationConsumer.as_asgi()),
    path('ws/chat/<sender_id>/<receiver_id>', Chating.as_asgi()),
    path('ws/chat/image/<sender_id>/<receiver_id>', BinaryConsumer.as_asgi())
]