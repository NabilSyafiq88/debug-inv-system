# Generated by Django 5.1.1 on 2024-10-17 07:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0012_remove_failure_info_completion_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='failure_info',
            name='completion_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]