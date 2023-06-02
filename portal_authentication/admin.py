from django.contrib import admin

from portal_authentication.models import Roles, User

# Register your models here.
admin.site.register(Roles)
admin.site.register(User)