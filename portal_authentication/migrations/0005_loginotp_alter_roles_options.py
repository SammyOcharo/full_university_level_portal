# Generated by Django 4.2.1 on 2023-06-03 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_authentication', '0004_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.IntegerField()),
                ('is_validated', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'login_otp',
            },
        ),
        migrations.AlterModelOptions(
            name='roles',
            options={'verbose_name_plural': 'roles'},
        ),
    ]
