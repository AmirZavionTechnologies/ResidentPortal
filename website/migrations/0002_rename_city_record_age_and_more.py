# Generated by Django 5.0.6 on 2024-06-03 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='city',
            new_name='Age',
        ),
        migrations.RenameField(
            model_name='record',
            old_name='state',
            new_name='Apartmentnumber',
        ),
        migrations.RenameField(
            model_name='record',
            old_name='zipcode',
            new_name='CNIC',
        ),
    ]
