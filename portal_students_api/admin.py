from django.contrib import admin

from portal_students_api.models import Student, StudentCourseInformation

# Register your models here.

admin.site.register(Student)
admin.site.register(StudentCourseInformation)