from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math
from django.db.models import Sum, Q

# Create your views here.

class ItemView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({'success': 0, 'message': 'Invalid Token'})

            inventory = request.query_params.get('inventory')
            if not inventory:
                return Response({'success': 0, 'message': 'Please provide inventory id'})

            filter_type = request.query_params.get('filter_type', None) 
            date_value = request.query_params.get('date_value', None)
            end_date_value = request.query_params.get('end_date_value', None) 

            if date_value:
                date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
            if end_date_value:
                end_date_value = datetime.strptime(end_date_value, '%Y-%m-%d').date()

            inventory_item = InventoryItem.objects.filter(inventory=inventory)

            inventory_logs_query = Q()

            if filter_type == 'daily':
                if not date_value:
                    date_value = timezone.now().date()
                inventory_logs_query &= Q(date_time__date=date_value)
            elif filter_type == 'weekly':
                if not date_value:
                    date_value = timezone.now().date()
                start_week = date_value - timedelta(days=date_value.weekday()) + timedelta(days=(6 - date_value.weekday()))
                end_week = start_week + timedelta(days=6)
                inventory_logs_query &= Q(date_time__date__range=[start_week, end_week])
            elif filter_type == 'monthly':
                if not date_value:
                    date_value = timezone.now().date()
                start_month = date_value.replace(day=1)
                end_month = start_month + relativedelta(months=1) - timedelta(days=1)
                inventory_logs_query &= Q(date_time__date__range=[start_month, end_month])
            elif filter_type == 'date':
                if date_value:
                    inventory_logs_query &= Q(date_time__date=date_value)
            elif filter_type == 'range':
                if date_value and end_date_value:
                    inventory_logs_query &= Q(date_time__date__range=[date_value, end_date_value])

            inventory_logs = InventoryLogs.objects.filter(item__inventory=inventory).filter(inventory_logs_query)
            ins = inventory_logs.filter(status='added').aggregate(total=Sum('count'))['total'] or 0
            outs = inventory_logs.filter(status='removed').aggregate(total=Sum('count'))['total'] or 0
            total = inventory_item.exclude(is_deleted=True).aggregate(total=Sum('count'))['total'] or 0
            inventory_item_serializer = ItemSerailizer(inventory_item, many=True)
            inventory_logs_serializer = FetchItemLogSerializer(inventory_logs, many=True)
            return Response({
                'success': 1,
                'data': {
                    'status': {
                        'ins': ins,
                        'outs': outs,
                        'total': total
                    },
                    'items': inventory_item_serializer.data,
                    'logs': inventory_logs_serializer.data
                }
            })
        except Exception as e:
            print(e)
        return Response({'success': 0, 'message': 'Something went wrong'})
    def patch(self,request):     
        try:
            if not request.user.is_authenticated:
                return Response({'success':0,'message':'Invalid Token'})
            item_id = self.request.query_params.get('item_id')
            if not item_id:
                return Response({'success':0,'message':'Please provide item id'})
            fields = ['count','action']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The field {field} should be provided'})
                data = request.data[field]
                if data == "" or data == None:
                    return Response({'success':0,'message':f'The field {field} cannot be empty or None'})
            action = request.data['action']
            if action == "remove":
                inventory_item = InventoryItem.objects.get(id=item_id)
                count = request.data['count']
                InventoryLogs.objects.create(
                    item = inventory_item,
                    status='removed',
                    count = count
                ).save()
                if count <= 0: 
                    return Response({'success':0,'message':'Cannot remove zero items'})
                if count > inventory_item.count:
                    return Response({'success':0,'message':'You dont have that much items'})
                inventory_item.count= inventory_item.count - count
                inventory_item.save()
                return Response({'success':1,'message':'Successfully Removed Item'})
            if action == "add":
                inventory_item = InventoryItem.objects.get(id=item_id)
                count = request.data['count']
                InventoryLogs.objects.create(
                    item = inventory_item,
                    status='added',
                    count = count
                ).save()
                if count <= 0: 
                    return Response({'success':0,'message':'Cannot remove zero items'})
                inventory_item.count= inventory_item.count + count
                inventory_item.save()
                return Response({'success':1,'message':'Successfully Added Item'})
        except InventoryItem.DoesNotExist:
            return Response({'message':'The item doesn\'t exist'})
        except Exception as e:
            # print(f"The exception is {e}")
            print(e)
            return Response({'success':0,'message':'Something went wrong'})
    def post(self,request):
        try:
            if not request.user.is_authenticated:
                return Response({'success':0,'message':'Invalid Token'})
            fields = ['inventory','name','image','count','price']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The field {field} should be provided'})
                if field == "" or field == None:
                    return Response({'success':0,'message':f'The field {field} cannot be null or empty'})
            item_serializer = ItemSerailizer(data=request.data)
            if item_serializer.is_valid():
                item = item_serializer.save()
                InventoryLogs.objects.create(item=item,status = 'added',count = item_serializer.data['count']).save()
                return Response({'success':1,'message':'Successfully added item'})
            return Response({'success':0,'message':'Error Saving data'})
        except Exception as e:
            print(e)
            return Response({'success':0,'message':'Something wen\'t wrong'})
    
    def delete(self,request):
        try:
            if not request.user.is_authenticated:
                return Response({'success':0,'message':'Invalid Token'})
            # self.request.query_params.get('item')
            item_id = self.request.query_params.get('item_id')
            if not item_id:
                return Response({'success':0,'message':'Please provide inventory id'})
            inventory_item = InventoryItem.objects.get(id=item_id)
            inventory_item.is_deleted = True
            InventoryLogs.objects.create(
                item = inventory_item,
                status='removed',
                count = inventory_item.count
            ).save()
            inventory_item.count= 0
            inventory_item.save()
            return Response({'success':1,'message':'Successfully Removed Item'})
        except InventoryItem.DoesNotExist:
            return Response({'message':'The item doesn\'t exist'})
        except Exception as e:
            # print(f"The exception is {e}")
            print(e)
            return Response({'success':0,'message':'Something went wrong'})