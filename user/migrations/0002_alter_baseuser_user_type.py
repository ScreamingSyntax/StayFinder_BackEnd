# Generated by Django 5.0.1 on 2024-02-17 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='user_type',
            field=models.CharField(choices=[('vendor', 'Vendor'), ('customer', 'Customer'), ('admin', 'Admin')], max_length=20),
        ),
    ]
