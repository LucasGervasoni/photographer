# Generated by Django 5.0.7 on 2024-08-13 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_crud', '0003_alter_order_appointment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_created_at',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
