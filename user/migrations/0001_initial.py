# Generated by Django 4.2.6 on 2023-10-20 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=10)),
                ('user_type', models.CharField(choices=[('vendor', 'Vendor'), ('customer', 'Customer')], max_length=20)),
                ('groups', models.ManyToManyField(related_name='baseuser_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='baseuser_set', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
