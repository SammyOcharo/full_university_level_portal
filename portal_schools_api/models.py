from django.db import models

# Create your models here.


class FacultySchool(models.Model):
    school_code = models.CharField(max_length=40)
    school_name = models.CharField(max_length=40)
    school_dean = models.CharField(max_length=50)
    school_description = models.CharField(max_length=255)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'school'

    def __str__(self) -> str:
        return f'{self.school_code}-{self.school_name}'
