from django.urls import path
from .views import *

urlpatterns = [
    path('',ItemView.as_view())
]
