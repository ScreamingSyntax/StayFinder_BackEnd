# Generated by Django 4.2.6 on 2023-11-11 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodation', '0002_room_kettle_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='coffee_powder_availability',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='hair_dryer_availability',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='milk_powder_availability',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='tea_powder_availability',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='tv_availability',
            field=models.BooleanField(null=True),
        ),
    ]
