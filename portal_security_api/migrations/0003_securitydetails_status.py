# Generated by Django 4.2.1 on 2023-06-23 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_security_api', '0002_roles_securitydetails_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='securitydetails',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]