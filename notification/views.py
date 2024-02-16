from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
from customer.models import *
from vendor.models import *
from user.models import BaseUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.db.models import Q


class NotificationAPIView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self, request):
        if request.user.is_authenticated:
            try:
                user = BaseUser.objects.get(email=request.user.email)
                is_customer = user.user_type == 'customer'
                is_vendor = user.user_type == 'vendor'
                if is_customer:
                    notifications = Notification.objects.filter(Q(customer__email=user.email) | Q(target='all') | Q(target='customer')).exclude(target='vendor')
                elif is_vendor:
                    notifications = Notification.objects.filter(Q(vendor__email=user.email) | Q(target='all') | Q(target='vendor')).exclude(target='customer')
                else:
                    notifications = Notification.objects.none()  # or handle non-customer/vendor users differently
                serializer = NotificationSerializer(notifications, many=True)
                return Response(serializer.data)
            except BaseUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        else:
            notifications = Notification.objects.filter(target='all')
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)