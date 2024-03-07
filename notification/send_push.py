import requests
from .models import NotificationDevice
from django.http import JsonResponse

def send_push_notification(users, title, message):
    print("dad")
    notification_devices = NotificationDevice.objects.filter(user__in=users).values_list('device_id', flat=True).distinct()
    print("dadada")
    # print(notification_devices)
    print(list(notification_devices))
    if(list(notification_devices) != []):
        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=AAAA1h72F4c:APA91bEbproe-z7MJqCNLn12XxpaKNrNLQ_YFmyWqPcjXS_xU_VHSWNV6emha775L8ESO-0ooTLvLJD24ut4dQZ42S8NAthEe9las7UjCv6kuXVwopALq_8aMuwgGo7cwErMSdbmUcy8', 
        }
        payload = {
            "registration_ids": list(notification_devices),
            "priority": "HIGH",
            "data": {
                "id": "2",
                "type": "msg"
            },
            "notification": {
                "title": title,
                "body": message
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Notification sent")
            # return JsonResponse({"message": "Notification sent successfully."}, status=200)
        else:
            print(response.json)
            print("Notification failed")
            # return JsonResponse({"error": "Failed to send notification."}, status=response.status_code)
