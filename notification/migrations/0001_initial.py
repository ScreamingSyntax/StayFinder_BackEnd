# Generated by Django 5.0.1 on 2024-02-16 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('vendor', '0005_alter_vendorprofile_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificatio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('is_seen', models.BooleanField(default=False)),
                ('notification_type', models.CharField(choices=[('warning', 'Warning'), ('info', 'Info'), ('success', 'Success'), ('failure', 'Failure')], max_length=20, null=True)),
                ('target', models.CharField(choices=[('all', 'All'), ('customer', 'Customer'), ('vendor', 'Vendor')], max_length=20, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.vendoruser')),
            ],
        ),
    ]
