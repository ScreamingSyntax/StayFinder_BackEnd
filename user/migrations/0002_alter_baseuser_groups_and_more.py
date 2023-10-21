# Generated by Django 4.2.6 on 2023-10-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='vendor_groups', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='vendors', to='auth.permission'),
        ),
    ]
