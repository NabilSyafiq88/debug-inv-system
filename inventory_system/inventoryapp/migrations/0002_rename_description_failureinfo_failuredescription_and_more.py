# Generated by Django 5.1.1 on 2024-10-07 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='failureinfo',
            old_name='description',
            new_name='failureDescription',
        ),
        migrations.RenameField(
            model_name='failureinfo',
            old_name='name',
            new_name='model',
        ),
        migrations.RenameField(
            model_name='failureinfo',
            old_name='category',
            new_name='testStation',
        ),
        migrations.RenameField(
            model_name='getdebugdata',
            old_name='product',
            new_name='info',
        ),
    ]
