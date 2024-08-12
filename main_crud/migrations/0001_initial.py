# Generated by Django 5.0.7 on 2024-08-12 22:32

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
                ('customer', models.CharField(max_length=150, verbose_name='Customer')),
                ('scheduled', models.DateTimeField(null=True, verbose_name='Scheduled')),
                ('address', models.CharField(max_length=200, verbose_name='Address')),
                ('services', multiselectfield.db.fields.MultiSelectField(choices=[('Drone', 'Drone'), ('Photo', 'Photo'), ('3d scan', '3d scan'), ('Vídeo', 'Vídeo'), ('Floor Plan', 'Floor Plan')], max_length=36)),
                ('order_status', models.CharField(choices=[('Not Uploaded', 'Not Uploaded'), ('Production', 'Production'), ('Completed', 'Completed')], default='Not Uploaded', verbose_name='Status')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
