# Generated by Django 4.2.1 on 2023-06-04 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal_schools_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facultyschool',
            old_name='name',
            new_name='school_name',
        ),
        migrations.AlterModelTable(
            name='facultyschool',
            table='school',
        ),
    ]