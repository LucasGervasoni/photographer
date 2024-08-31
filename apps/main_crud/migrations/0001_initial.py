# Generated by Django 5.0.7 on 2024-08-31 03:12

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
                ('order_created_at', models.DateTimeField(auto_created=True, editable=False, verbose_name='Created At')),
                ('appointment_team_members', models.CharField(max_length=300, verbose_name='Appointment Member')),
                ('customer', models.CharField(blank=True, max_length=200, null=True, verbose_name='Customer')),
                ('appointment_date', models.DateTimeField(max_length=200, null=True, verbose_name='Scheduled')),
                ('address', models.CharField(max_length=200, verbose_name='Address')),
                ('appointment_items', models.CharField(max_length=200, verbose_name='Services')),
                ('order_status', models.CharField(choices=[('Not Uploaded', 'Not Uploaded'), ('Production', 'Production'), ('Completed', 'Completed')], default='Not Uploaded', max_length=150, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='OrderEditorAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
