# Generated by Django 5.0.7 on 2024-08-18 16:55

import django.db.models.deletion
import multiselectfield.db.fields
import pictures.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_crud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderImageGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('editor_note', models.TextField(blank=True, null=True)),
                ('services', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Drone Vídeo', 'Drone Vídeo'), ('Drone Photo', 'Drone Photo'), ('Photo', 'Photo'), ('3d scan', '3d scan'), ('Video', 'Video'), ('Floor Plan', 'Floor Plan')], max_length=54)),
                ('scan_url', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_crud.order')),
            ],
            options={
                'verbose_name': 'Order File Created ',
                'verbose_name_plural': 'Order Files Created',
            },
        ),
        migrations.CreateModel(
            name='OrderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to=pictures.models.order_image_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('photos_sent', models.CharField(verbose_name='Assets to be uploaded')),
                ('photos_returned', models.CharField(verbose_name='Assets to be returned')),
                ('converted_image', models.ImageField(blank=True, null=True, upload_to='converted_images/')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='main_crud.order')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pictures.orderimagegroup')),
            ],
            options={
                'verbose_name': 'File uploaded',
                'verbose_name_plural': 'Files uploaded',
            },
        ),
        migrations.CreateModel(
            name='UserAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('download', 'Download'), ('upload', 'Upload')], max_length=50)),
                ('action_date', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_crud.order')),
                ('order_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pictures.orderimage')),
            ],
        ),
    ]
