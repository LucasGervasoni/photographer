# Generated by Django 5.0.7 on 2024-07-26 00:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_perfil_addressone_remove_perfil_addresstwo_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=150)),
                ('lastName', models.CharField(max_length=150)),
                ('phoneOne', models.CharField(max_length=100)),
                ('phoneTwo', models.CharField(max_length=100)),
                ('addressOne', models.CharField(max_length=150, verbose_name='Address 1')),
                ('addressTwo', models.CharField(max_length=150, verbose_name='Address 2')),
                ('zipCode', models.CharField(max_length=50, verbose_name='Zip Code')),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Perfil',
        ),
    ]
