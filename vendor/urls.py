from django.urls import path
from vendor.views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('unverifiedProfiles/',ViewUnverifiedProfiles.as_view()),
    path('resetPass/',ResetPassword.as_view()),
    path('forgotPass/',ForgotPassword.as_view()),
    path('signup/',SignUpView.as_view()),
    path('data/',GetVendorData.as_view()),
    path('verifedData/',VendorVerificationData.as_view()),
    path('acceptVendorProfile/',VendorAcceptData.as_view()),
    path('rejectVendorProfile/',VendorRejectData.as_view()),
]