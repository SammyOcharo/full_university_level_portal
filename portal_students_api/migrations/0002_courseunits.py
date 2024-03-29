# Generated by Django 4.1.7 on 2023-07-12 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_students_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=100)),
                ('unit_code', models.CharField(max_length=100)),
                ('unit_description', models.CharField(max_length=100)),
                ('unit_instructor', models.CharField(max_length=100)),
                ('unit_schedule', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'course_unit',
            },
        ),
    ]
