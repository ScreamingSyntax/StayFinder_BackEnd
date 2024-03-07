# Generated by Django 5.0.1 on 2024-03-06 15:31

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accomodation', '0009_room_room_count_alter_accommodation_monthly_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accomodation.accommodation')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='')),
                ('count', models.IntegerField()),
                ('price', models.IntegerField()),
                ('date_field', models.DateField()),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.inventory')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=datetime.datetime(2024, 3, 6, 21, 16, 56, 618882))),
                ('status', models.CharField(choices=[('added', 'Added'), ('removed', 'Removed')], max_length=20, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.inventoryitem')),
            ],
        ),
    ]
