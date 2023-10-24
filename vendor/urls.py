from django.urls import path
from vendor.views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('signup/',SignUpView.as_view()),
    path('data/',GetVendorData.as_view()),
    path('verifedData/',VendorVerificationData.as_view()),

]