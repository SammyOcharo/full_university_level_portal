# Generated by Django 4.1.7 on 2023-07-13 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal_students_api', '0004_enrollment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gradings', to='portal_students_api.student')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gradings', to='portal_students_api.courseunits')),
            ],
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weightage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='portal_students_api.courseunits')),
            ],
        ),
    ]
