# Generated by Django 4.2.7 on 2023-11-09 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_driver_car_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cargo_size',
            field=models.PositiveIntegerField(default=100, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='car_space',
            field=models.PositiveIntegerField(default=5000, max_length=100),
            preserve_default=False,
        ),
    ]
