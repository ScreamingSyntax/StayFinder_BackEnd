from django.urls import path,include
from tier.views import *

urlpatterns = [
    path('',GetTierInformation.as_view()),
    path('currentTier/',GetCurrenTierInformation.as_view()),
    path('transactionHistory/',TransactionHistory.as_view()),
    path('renewTier/',RenewTier.as_view()),
    path('admin/',TierView.as_view())
]
