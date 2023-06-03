from django.contrib import admin

from portal_authentication.models import LoginOtp, Roles, User

# Register your models here.
admin.site.register(Roles)
admin.site.register(User)
admin.site.register(LoginOtp)