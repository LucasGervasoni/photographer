# Generated by Django 5.0.7 on 2024-08-01 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0004_alter_image_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='photo',
            field=models.ImageField(upload_to='media'),
        ),
    ]
