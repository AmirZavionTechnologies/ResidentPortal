# Generated by Django 5.0.6 on 2024-06-04 07:07

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_guard'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(max_length=50)),
                ('vehicle_model', models.CharField(max_length=50)),
                ('car_number_plate', models.CharField(max_length=150)),
                ('carmodel', models.CharField(max_length=100, null=True, unique=True)),
                ('entry_codes', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='website.resident')),
            ],
        ),
    ]