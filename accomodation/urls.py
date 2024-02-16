from django.urls import path
from accomodation.views import *
urlpatterns = [
    path('rental_room/',RentalRoom.as_view()),
    
    path('rental_room/image/',RentalRoomImage.as_view()),
    path('rental_room/room/',RentalRoomRoomUpdate.as_view()),
    path('hostel/room/image/',HostelImageRooms.as_view()),
    path('',AccommodationView.as_view()),
    path('display/',ShowAccommodations.as_view()),
    path('display/accommodation/',ShowParticularAccommodation.as_view()),
    path('verify/',VerifyAccommodation.as_view()),
    path('hostel/',HostelAccommodation.as_view()),
    path('hostel/room/',HostelRooms.as_view()),
    path('hotel/',HotelAccommodation.as_view()),
    path('hotel/tier/',HotelTierBased.as_view()),
    path('hotel/tier/update/',HotelTierBasedAccommodation.as_view()),
    path('hotel/nonTier/',HotelNonTierBased.as_view()),
    path('hotel/nonTier/room/',HotelNonTierBasedRoom.as_view()),
    path('hotel/tier/room/',HotelTierBasedRoom.as_view()),
    path('search/',SearchAccommodation.as_view()),
    path('reVerify/',VerificationResubmit.as_view()),
]
