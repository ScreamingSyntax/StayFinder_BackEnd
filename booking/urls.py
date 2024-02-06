from django.urls import path
from .views import *

urlpatterns = [
    path('',BookingView.as_view()),
    path('request/',BookingRequestView.as_view()),
    path('request/verify/',VerifyBookingRequest.as_view())
]

