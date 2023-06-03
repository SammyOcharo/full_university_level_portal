from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import USER_ROLES
# Create your models here.


class Roles(models.Model):
    name = models.CharField(max_length=20, null=False)
    short_name = models.CharField(choices=USER_ROLES, default='', max_length=20, unique=True, blank=False)
    is_active = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.short_name
    
    class Meta:
        verbose_name_plural = 'roles'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    id_number = models.CharField(max_length=9, unique=True, blank=False)
    username = models.EmailField(unique=True, null=False)
    role = models.ForeignKey(Roles, on_delete=models.DO_NOTHING, related_name='user_role', null=True)
    status = models.IntegerField(default=0)
    full_name = models.CharField(max_length=30)

    class Meta:
        db_table = 'user'

    def __str__(self) -> str:
        return self.email
    

class LoginOtp(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    is_validated = models.IntegerField(default=0)

    class Meta:
        db_table = 'login_otp'

    def __str__(self):
        return self.email


class PasswordResetOtp(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    is_validated = models.IntegerField(default=0)

    class Meta:
        db_table = 'password_reset_otp'

    def __str__(self):
        return self.email