# Generated by Django 5.0.7 on 2024-08-16 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0002_alter_orderimagegroup_services'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderimage',
            options={'verbose_name': 'File uploaded', 'verbose_name_plural': 'Files uploaded'},
        ),
        migrations.AlterModelOptions(
            name='orderimagegroup',
            options={'verbose_name': 'Order File Created ', 'verbose_name_plural': 'Order Files Created'},
        ),
    ]
