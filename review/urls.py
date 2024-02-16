from django.urls import path,include
from .views import *
urlpatterns = [
    path('',Reviews.as_view()),
    path('vendor/',ViewVendorReviews.as_view()),
    path('customer/',ViewCustomerReviews.as_view()),
    path('toReview/',ViewToReviewReviews.as_view()),
    # path('')
]
