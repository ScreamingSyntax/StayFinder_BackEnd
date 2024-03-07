# myproject/routing.py
from django.urls import path
# from order.consumers import *
from notification.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/notification/', NotificationConsumer.as_asgi()),

]