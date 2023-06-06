from django.db import models

from portal_schools_api.models import FacultySchool

# Create your models here.

class SchoolFacultyDepartment(models.Model):
    school = models.ForeignKey(FacultySchool, on_delete=models.DO_NOTHING)
    department_name = models.CharField(max_length=30)
    department_code = models.CharField(max_length=40)
    department_chairman = models.CharField(max_length=50)
    department_description = models.CharField(max_length=100)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'school_department'

    def __str__(self):
        return self.department_name