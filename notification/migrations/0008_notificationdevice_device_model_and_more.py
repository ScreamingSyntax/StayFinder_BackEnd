# Generated by Django 5.0.1 on 2024-02-28 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0007_alter_notification_added_date_notificationdevice'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationdevice',
            name='device_model',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 28, 13, 12, 15, 339232)),
        ),
    ]