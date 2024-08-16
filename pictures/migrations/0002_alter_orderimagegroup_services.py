# Generated by Django 5.0.7 on 2024-08-16 14:18

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderimagegroup',
            name='services',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Drone Vídeo', 'Drone Vídeo'), ('Drone Photo', 'Drone Photo'), ('Photo', 'Photo'), ('3d scan', '3d scan'), ('Video', 'Video'), ('Floor Plan', 'Floor Plan')], max_length=54),
        ),
    ]
