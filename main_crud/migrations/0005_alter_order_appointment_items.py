# Generated by Django 5.0.7 on 2024-08-13 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_crud', '0004_alter_order_appointment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='appointment_items',
            field=models.CharField(max_length=200, verbose_name='Appointment Items'),
        ),
    ]
