from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import USER_ROLES
# Create your models here.


class Roles(models.Model):
    name = models.CharField(max_length=20, null=False)
    short_name = models.CharField(choices=USER_ROLES, default='', max_length=20, unique=True, blank=False)
    is_active = models.IntegerField(default=0)


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    mobile_number = models.CharField(max_length=15, null=False)
    id_number = models.CharField(max_length=9, null=False, unique=True, blank=False)
    username = models.EmailField(unique=True, null=False)
    date_of_birth = models.DateTimeField()
    role = models.ForeignKey(Roles, on_delete=models.DO_NOTHING, related_name='user_role', null=False)
    status = models.IntegerField(default=0)
    full_name = models.CharField(max_length=30, null=False)
