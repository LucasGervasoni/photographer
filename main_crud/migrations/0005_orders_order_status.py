# Generated by Django 5.0.7 on 2024-08-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_crud', '0004_alter_orders_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('Not Uploaded', 'Not Uploaded'), ('Production', 'Production'), ('Completed', 'Completed')], default='Not Uploaded', verbose_name='Status'),
        ),
    ]
