# Generated by Django 5.1.1 on 2024-10-17 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0011_rename_fg_model_failure_info_root_cause_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='failure_info',
            name='completion_date',
        ),
    ]
