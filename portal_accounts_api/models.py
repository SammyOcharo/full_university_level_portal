from django.db import models
from django.contrib.auth import get_user_model

from portal_students_api.models import Student
User = get_user_model()

# Create your models here.

class UniversityAccounts(models.Model):
    accounts_code = models.CharField(max_length=50)
    bank_account = models.EmailField()
    bank_name = models.CharField(max_length=30)
    # student = models.ForeignKey(Student)

    def __str__(self) -> str:
        return self.accounts_code
    
    class Meta:
        db_table = 'accounts'
