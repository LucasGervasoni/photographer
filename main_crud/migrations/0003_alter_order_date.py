# Generated by Django 5.0.7 on 2024-08-07 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_crud', '0002_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
