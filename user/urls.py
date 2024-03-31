from django.urls import path
from .views import *
urlpatterns = [
    path('dashboard/',DashBoardDetails.as_view()),
    path('login/',AdminLogin.as_view()),
    path('unverifiedAccommodations/',ViewUnverifiedAccommodations.as_view()),
    path('accommodationParticular/',ViewAccommodationDetail.as_view())
]
