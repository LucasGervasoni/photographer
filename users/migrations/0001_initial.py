# Generated by Django 5.0.7 on 2024-08-13 14:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100, null=True, verbose_name='First Name')),
                ('lastName', models.CharField(max_length=100, null=True, verbose_name='Last Name')),
                ('phoneOne', models.CharField(max_length=100, verbose_name='Phone 1')),
                ('phoneTwo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone 2')),
                ('address', models.CharField(max_length=300, verbose_name='Address')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
