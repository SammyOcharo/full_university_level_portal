# Generated by Django 4.2.1 on 2023-06-06 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal_school_department_api', '0002_schoolfacultydepartment_department_description'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='schoolfacultydepartment',
            table='school_department',
        ),
    ]