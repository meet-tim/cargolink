# Generated by Django 4.2.7 on 2023-11-08 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_trip_space_left'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='driver_license',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='driver',
            name='national_id',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='driver',
            name='passport_pic',
            field=models.CharField(max_length=200),
        ),
    ]