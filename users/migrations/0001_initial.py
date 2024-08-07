# Generated by Django 5.0.7 on 2024-08-07 15:11

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
                ('addressOne', models.CharField(max_length=150, verbose_name='Address 1')),
                ('addressTwo', models.CharField(blank=True, max_length=150, null=True, verbose_name='Address 2')),
                ('zipCode', models.CharField(blank=True, max_length=50, null=True, verbose_name='Zip Code')),
                ('city', models.CharField(help_text='Ex: San Francisco', max_length=50)),
                ('state', models.CharField(help_text='Ex: CA', max_length=50)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
