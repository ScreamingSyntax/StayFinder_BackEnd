from rest_framework import serializers
from .models import Notification,NotificationDevice

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationDevice
        fields = ['device_id','device_model']