# Generated by Django 5.1.1 on 2024-10-10 02:43

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='cells_Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_Name', models.CharField(max_length=100, null=True)),
                ('date_registered', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('1', 'ADMIN'), ('2', 'ENGTECH'), ('3', 'OPERATOR')], default=1, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='engTech',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Failure_Mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_Station', models.CharField(choices=[('PCA Burn IN', 'PCA Burn IN'), ('Calibration', 'Calibration'), ('Final Test', 'Final Test'), ('Temperature Test', 'Temperature Test'), ('Manual Test', 'Manual Test'), ('LCD Check', 'LCD Check'), ('Laser Alignment', 'Laser Alignment'), ('Manual Test', 'Manual Test')], max_length=20, null=True)),
                ('failure_Mode', models.CharField(max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('test_Cells', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventoryapp.cells_name')),
            ],
        ),
        migrations.CreateModel(
            name='Failure_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_Station', models.CharField(choices=[('PCA Burn IN', 'PCA Burn IN'), ('Calibration', 'Calibration'), ('Final Test', 'Final Test'), ('Temperature Test', 'Temperature Test'), ('Manual Test', 'Manual Test'), ('LCD Check', 'LCD Check'), ('Laser Alignment', 'Laser Alignment'), ('Manual Test', 'Manual Test')], max_length=20, null=True)),
                ('date_Registered', models.DateTimeField(auto_now_add=True)),
                ('test_Cells', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventoryapp.cells_name')),
                ('failure_Mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventoryapp.failure_mode')),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sku_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_Status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], max_length=20, null=True)),
                ('product_Model', models.CharField(max_length=100, null=True)),
                ('FG_PartNo', models.CharField(max_length=100, null=True)),
                ('FG_Model', models.CharField(max_length=100, null=True)),
                ('PCA_SN_Number', models.CharField(max_length=100, null=True)),
                ('test_Cells', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventoryapp.cells_name')),
            ],
        ),
    ]
