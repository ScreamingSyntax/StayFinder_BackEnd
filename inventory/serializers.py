from .models import *
from rest_framework.serializers import ModelSerializer


class ItemSerailizer(ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class ItemLogSerializer(ModelSerializer):
    class Meta:
        model = InventoryLogs
        fields = "__all__"


class FetchItemLogSerializer(ModelSerializer):
    item = ItemSerailizer()
    class Meta:
        model = InventoryLogs
        fields =  ['item','date_time','status','count']

