# Generated by Django 4.2.6 on 2023-10-23 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_alter_vendorprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorprofile',
            name='digital_signature',
            field=models.ImageField(default='signature.png', upload_to=''),
        ),
    ]
