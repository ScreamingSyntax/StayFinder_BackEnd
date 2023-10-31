# Generated by Django 4.2.6 on 2023-10-31 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0005_alter_vendorprofile_vendor'),
        ('tier', '0002_currenttier_paid_till'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.BooleanField()),
                ('method_of_payment', models.CharField(max_length=10)),
                ('paid_date', models.DateTimeField(auto_now=True)),
                ('paid_till', models.DateTimeField()),
                ('tier_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tier.tier')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vendor.vendoruser')),
            ],
        ),
    ]
