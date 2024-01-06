from django.urls import path,include
from customer.views import *
urlpatterns = [
    path('',CustomerView.as_view())
]
