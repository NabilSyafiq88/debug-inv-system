# Generated by Django 5.1.2 on 2024-11-01 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0019_root_cause'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action_taken',
            name='date_registered',
        ),
        migrations.RemoveField(
            model_name='cells_name',
            name='date_registered',
        ),
        migrations.RemoveField(
            model_name='failure_mode',
            name='date',
        ),
        migrations.RemoveField(
            model_name='model_name',
            name='date_registered',
        ),
        migrations.RemoveField(
            model_name='root_cause',
            name='date_registered',
        ),
        migrations.RemoveField(
            model_name='station_name',
            name='date_registered',
        ),
    ]
