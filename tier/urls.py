from django.urls import path,include
from tier.views import *

urlpatterns = [
    path('',GetTierInformation.as_view())
]