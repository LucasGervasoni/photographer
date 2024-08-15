# Generated by Django 5.0.7 on 2024-08-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_team_members', models.CharField(max_length=300, verbose_name='Appointment Member')),
                ('customer', models.CharField(max_length=200, verbose_name='Customer')),
                ('appointment_date', models.CharField(null=True, verbose_name='Scheduled')),
                ('address', models.CharField(max_length=200, verbose_name='Address')),
                ('appointment_items', models.CharField(max_length=200, verbose_name='Services')),
                ('order_status', models.CharField(choices=[('Not Uploaded', 'Not Uploaded'), ('Production', 'Production'), ('Completed', 'Completed')], default='Not Uploaded', verbose_name='Status')),
                ('order_created_at', models.CharField(editable=False, verbose_name='Created At')),
            ],
        ),
    ]
