# Generated by Django 4.2.6 on 2023-10-31 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_payment_paid_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='transaction_id',
            field=models.TextField(null=True),
        ),
    ]