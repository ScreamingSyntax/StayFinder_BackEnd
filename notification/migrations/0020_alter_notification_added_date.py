# Generated by Django 5.0.1 on 2024-03-22 08:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0019_alter_notification_added_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 22, 14, 35, 11, 946479)),
        ),
    ]