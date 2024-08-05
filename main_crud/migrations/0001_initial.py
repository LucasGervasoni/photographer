# Generated by Django 5.0.7 on 2024-08-05 20:08

import django.db.models.deletion
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled', models.DateField(null=True, verbose_name='Scheduled')),
                ('time', models.TimeField()),
                ('addressOne', models.CharField(max_length=150, verbose_name='Address 1')),
                ('addressTwo', models.CharField(blank=True, max_length=150, null=True, verbose_name='Address 2')),
                ('zipCode', models.CharField(blank=True, max_length=50, null=True, verbose_name='Zip Code')),
                ('city', models.CharField(help_text='Ex: San Francisco', max_length=50)),
                ('state', models.CharField(help_text='Ex: CA', max_length=50)),
                ('services', multiselectfield.db.fields.MultiSelectField(choices=[('Drone', 'Drone'), ('Photo', 'Photo'), ('3d scan', '3d scan'), ('Vídeo', 'Vídeo')], max_length=25)),
                ('order_status', models.CharField(choices=[('Not Uploaded', 'Not Uploaded'), ('Production', 'Production'), ('Completed', 'Completed')], default='Not Uploaded', verbose_name='Status')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
