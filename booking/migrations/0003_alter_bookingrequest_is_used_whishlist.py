# Generated by Django 5.0.1 on 2024-02-08 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodation', '0009_room_room_count_alter_accommodation_monthly_rate'),
        ('booking', '0002_bookingrequest_is_used'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingrequest',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='WhishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accomodation.accommodation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]