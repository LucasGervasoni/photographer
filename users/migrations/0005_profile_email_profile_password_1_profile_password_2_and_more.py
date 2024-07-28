# Generated by Django 5.0.7 on 2024-07-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_delete_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(default=' ', max_length=150, verbose_name='E-mail'),
        ),
        migrations.AddField(
            model_name='profile',
            name='password_1',
            field=models.CharField(default=' ', max_length=70, verbose_name='Password'),
        ),
        migrations.AddField(
            model_name='profile',
            name='password_2',
            field=models.CharField(default=' ', max_length=70, verbose_name='Repeat your Password'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=50, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='firstName',
            field=models.CharField(max_length=150, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lastName',
            field=models.CharField(max_length=150, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phoneOne',
            field=models.CharField(max_length=100, verbose_name='Phone 1'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phoneTwo',
            field=models.CharField(max_length=100, verbose_name='Phone 2'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(max_length=50, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=150, verbose_name='Username'),
        ),
    ]
