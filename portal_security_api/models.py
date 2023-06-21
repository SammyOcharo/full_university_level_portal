from django.db import models

from portal_students_api.models import Student

# Create your models here.

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