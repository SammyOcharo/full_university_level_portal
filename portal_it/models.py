from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ITAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    id_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=30)
    school_id_number = models.CharField(max_length=10)
    email = models.EmailField()
    status = models.IntegerField()

    class Meta:
        db_table = 'it_admin'

    def __str__(self):
        return self.full_name



class ITAdminActivationOtp(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    is_validated = models.IntegerField(default=0)

    class Meta:
        db_table = 'it_admin_activation_otp'

    def __str__(self):
        return self.email
