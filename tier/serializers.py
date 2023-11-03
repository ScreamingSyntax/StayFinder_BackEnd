from rest_framework import serializers
from tier.models import *

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = "__all__"

class TransactionTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TierTransaction
        fields="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TierTransaction
        fields = ('tier','paid_amount','paid_date')
    
