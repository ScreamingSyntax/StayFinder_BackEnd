# Generated by Django 4.2.6 on 2023-12-09 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodation', '0005_alter_room_washroom_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='per_day_rent',
            field=models.IntegerField(null=True),
        ),
    ]
