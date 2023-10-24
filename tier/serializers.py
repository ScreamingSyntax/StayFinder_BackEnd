from rest_framework import serializers
from tier.models import *

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = "__all__"

class CurrentTierSerailzer(serializers.ModelSerializer):
    class Meta:
        model = CurrentTier
        fields="__all__"