# Generated by Django 4.2.6 on 2023-10-21 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_baseuser_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_accepted',
            field=models.BooleanField(null=True),
        ),
    ]