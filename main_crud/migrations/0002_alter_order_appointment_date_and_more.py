# Generated by Django 5.0.7 on 2024-08-13 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_crud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='appointment_date',
            field=models.CharField(null=True, verbose_name='Appointment Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_created_at',
            field=models.CharField(verbose_name='Created At'),
        ),
    ]
