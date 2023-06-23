from django.db import models
from portal_security_api.choices import USER_ROLES

from portal_students_api.models import Student

# Create your models here.
class Roles(models.Model):
    name = models.CharField(max_length=20, null=False)
    short_name = models.CharField(choices=USER_ROLES, default='', max_length=20, unique=True, blank=False)
    is_active = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.short_name
    
    class Meta:
        verbose_name_plural = 'security_roles'

class EntryLog(models.Model):
    student =  models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(auto_now_add=True)
    entry_point = models.CharField(max_length=50)

    class Meta:
        db_table = 'entry_logs'
        verbose_name_plural = 'entry_logs'

    def __str__(self) -> str:
        return self.student.student_name
    
class SecurityDetails(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    employee_id = models.CharField(max_length=50)
    employee_photo = models.ImageField()
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'security_details'
        verbose_name_plural = 'security_details'

    def __str__(self) -> str:
        return self.first_name