# Generated by Django 4.2.7 on 2023-11-08 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_driver_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='car_picture',
            field=models.CharField(max_length=200),
        ),
    ]