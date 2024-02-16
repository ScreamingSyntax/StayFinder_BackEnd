from django.urls import path,include
from customer.views import *
urlpatterns = [
    path('',CustomerView.as_view()),
    path('reset/',ResetPassword.as_view()),
    path('forgotPass/',ForgotPassword.as_view())
]
