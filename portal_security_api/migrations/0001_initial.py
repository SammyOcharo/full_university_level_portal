# Generated by Django 4.1.7 on 2023-07-12 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntryLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_time', models.DateTimeField(auto_now_add=True)),
                ('exit_time', models.DateTimeField(auto_now_add=True)),
                ('entry_point', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'entry_logs',
                'db_table': 'entry_logs',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('short_name', models.CharField(choices=[('security_admin', 'security_admin'), ('security', 'security')], default='', max_length=20, unique=True)),
                ('is_active', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'security_roles',
            },
        ),
        migrations.CreateModel(
            name='SecurityAdminActivationOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('otp', models.IntegerField()),
                ('is_validated', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'security_admin_activation_otp',
            },
        ),
        migrations.CreateModel(
            name='SecurityDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('employee_id', models.CharField(max_length=50)),
                ('employee_photo', models.ImageField(upload_to='')),
                ('status', models.IntegerField(default=0)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portal_security_api.roles')),
            ],
            options={
                'verbose_name_plural': 'security_details',
                'db_table': 'security_details',
            },
        ),
    ]
