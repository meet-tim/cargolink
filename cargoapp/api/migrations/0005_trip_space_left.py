# Generated by Django 4.2.7 on 2023-11-08 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_trip_passengers_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='space_left',
            field=models.PositiveIntegerField(default=5000, max_length=5000),
        ),
    ]
