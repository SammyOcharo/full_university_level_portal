from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from portal_authentication.models import LoginOtp, Roles, User

class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ('username', 'is_active', 'role',
                    'is_staff')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        ('Personal info', {'fields': (
            'username','first_name', 'last_name', 'email', 'mobile_number','id_number')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',
                                    'is_active','role', 'status')}),
    )

    search_fields = ('email', 'username','mobile_number')


admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Roles)
admin.site.register(LoginOtp)