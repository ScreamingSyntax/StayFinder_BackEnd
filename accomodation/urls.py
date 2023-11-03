from django.urls import path
from accomodation.views import *
urlpatterns = [
    path('addRentalRoom/',RentalRoom.as_view())
]
