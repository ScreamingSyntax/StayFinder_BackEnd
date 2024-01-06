# Generated by Django 4.2.6 on 2023-11-23 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodation', '0004_alter_room_washroom_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='washroom_status',
            field=models.CharField(choices=[('Excellent', 'excellent'), ('Average', 'average'), ('Adjustable', 'adjustable')], max_length=20, null=True),
        ),
    ]