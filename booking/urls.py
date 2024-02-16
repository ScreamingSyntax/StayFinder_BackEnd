from django.urls import path
from .views import *

urlpatterns = [
    path('',BookingView.as_view()),
    path('book/history/',ViewBookingHistory.as_view()),
    path('wishlist/',WishListView.as_view()),
    path('request/history/',ViewBookingRequestHistory.as_view()),
    path('details/',ViewParticularBookingDetails.as_view()),
    path('request/',BookingRequestView.as_view()),
    path('request/verify/',VerifyBookingRequest.as_view()),
    path('revenue/',RevenueView.as_view())
]

