# Generated by Django 4.2.6 on 2023-10-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_baseuser_is_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='is_accepted',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
