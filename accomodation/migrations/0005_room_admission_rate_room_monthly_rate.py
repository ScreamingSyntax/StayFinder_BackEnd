# Generated by Django 4.2.6 on 2023-11-03 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodation', '0004_alter_room_washroom_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='admission_rate',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='monthly_rate',
            field=models.IntegerField(null=True),
        ),
    ]