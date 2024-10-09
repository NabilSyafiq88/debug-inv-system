# Generated by Django 5.1.1 on 2024-10-09 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0014_alter_sku_info_test_cells'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='failure_mode',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='failure_mode',
            name='info',
        ),
        migrations.RemoveField(
            model_name='failure_mode',
            name='order_quantity',
        ),
        migrations.AddField(
            model_name='failure_mode',
            name='test_Cells',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventoryapp.cells_name'),
        ),
        migrations.AddField(
            model_name='failure_mode',
            name='test_Station',
            field=models.CharField(choices=[('PCA Burn IN', 'PCA Burn IN'), ('Calibration', 'Calibration'), ('Final Test', 'Final Test'), ('Temperature Test', 'Temperature Test'), ('Manual Test', 'Manual Test'), ('LCD Check', 'LCD Check'), ('Laser Alignment', 'Laser Alignment'), ('Manual Test', 'Manual Test')], max_length=20, null=True),
        ),
    ]
