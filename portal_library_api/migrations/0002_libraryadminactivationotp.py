# Generated by Django 4.2.1 on 2023-06-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_library_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryAdminActivationOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('otp', models.IntegerField()),
                ('is_validated', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'library_admin_activation_otp',
            },
        ),
    ]