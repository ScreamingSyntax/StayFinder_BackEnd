# Generated by Django 5.0.1 on 2024-03-07 08:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0015_alter_notification_added_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 14, 17, 52, 58594)),
        ),
    ]
