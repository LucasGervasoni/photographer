# Generated by Django 5.0.7 on 2024-08-16 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0003_alter_orderimage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderimage',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='previews/'),
        ),
    ]
