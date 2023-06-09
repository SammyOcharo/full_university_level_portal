from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class UniversityAccounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    accounts_email = models.EmailField()
    accounts_name = models.CharField(max_length=30)
    accounts_Id = models.CharField(max_length=8)

    def __str__(self) -> str:
        return self.accounts_name
    
    class Meta:
        db_table = 'accounts'
