# Generated by Django 4.2.6 on 2023-10-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_baseuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='otp',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
