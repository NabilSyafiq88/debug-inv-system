# Generated by Django 5.1.2 on 2024-10-29 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0015_alter_failure_info_failure_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failure_mode',
            name='test_Station',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sku_info',
            name='product_Status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]