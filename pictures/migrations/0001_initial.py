# Generated by Django 5.0.7 on 2024-08-12 22:32

import django.core.validators
import django.db.models.deletion
import multiselectfield.db.fields
import pictures.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_crud', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to=pictures.models.order_image_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('editor_note', models.TextField(blank=True, null=True)),
                ('selected_service', multiselectfield.db.fields.MultiSelectField(choices=[('Drone', 'Drone'), ('Photo', 'Photo'), ('3d scan', '3d scan'), ('Vídeo', 'Vídeo'), ('Floor Plan', 'Floor Plan')], max_length=100)),
                ('scan_url', models.URLField(blank=True, null=True, validators=[django.core.validators.URLValidator()])),
                ('photos_sent', models.IntegerField(default=0)),
                ('photos_returned', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='main_crud.order')),
            ],
        ),
        migrations.CreateModel(
            name='UserAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('download', 'Download'), ('upload', 'Upload')], max_length=50)),
                ('action_date', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_crud.order')),
                ('order_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pictures.orderimage')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
