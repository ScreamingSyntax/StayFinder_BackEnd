# Generated by Django 4.2.6 on 2023-10-31 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_vendorprofile_vendor'),
        ('tier', '0002_alter_transaction_method_of_payment_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transaction',
            new_name='TierTransaction',
        ),
    ]
