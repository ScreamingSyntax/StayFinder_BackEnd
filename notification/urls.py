from django.urls import path
from .views import *
urlpatterns = [
    path('',NotificationAPIView.as_view()),
    path('registerDevice/',RegisterDevice.as_view())
]
