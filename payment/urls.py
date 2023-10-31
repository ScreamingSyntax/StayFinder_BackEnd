from django.urls import path,include
from .views import *
urlpatterns=[
    path('',GetVendorPaymentData.as_view())
]