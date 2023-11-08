# Generated by Django 4.2.7 on 2023-11-08 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_trip_driver_alter_trip_passengers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='passengers',
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.PositiveIntegerField(max_length=200)),
                ('full_name', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=100)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.trip')),
            ],
        ),
    ]