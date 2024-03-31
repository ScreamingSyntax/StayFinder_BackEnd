from django.urls import path,include
from .views import *
urlpatterns = [
    path('',GetMessages.as_view()),
    path('search/',SearchMessages.as_view()),
    path('all/',GetMainScreenMessages.as_view()),
    path('searchReceivers/',GetSearchMessages.as_view()),


]
