# Generated by Django 4.2.6 on 2023-10-20 07:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorUser',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.baseuser')),
                ('is_verified', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=datetime.datetime.now)),
                ('date_verified', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('user.baseuser',),
        ),
    ]
