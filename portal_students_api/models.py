from django.db import models
from django.contrib.auth import get_user_model
from portal_school_department_api.models import SchoolFacultyDepartment

from portal_schools_api.models import FacultySchool
User = get_user_model()

#Course Information model
class StudentCourseInformation(models.Model):
    course_name = models.CharField(max_length=50)
    course_ID = models.CharField(max_length=50)
    course_description = models.CharField(max_length=255)
    course_duration = models.CharField(max_length=50)
    course_instructor = models.CharField(max_length= 100)

    class Meta:
        db_table = 'student_course'

    def __str__(self):
        return self.course_name
    
# Unit Information
class CourseUnits(models.Model):
    unit_name = models.CharField(max_length=100)
    unit_code = models.CharField(max_length=100)
    unit_description = models.CharField(max_length=100)
    unit_instructor = models.CharField(max_length=100)
    unit_schedule = models.CharField(max_length=100)

    class Meta:
        db_table = 'course_unit'

    def __str__(self):
        return self.unit_name

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    student_name = models.CharField(max_length=50)
    national_id_number = models.CharField(max_length=9)
    school = models.ForeignKey(FacultySchool, on_delete=models.DO_NOTHING)
    department = models.ManyToManyField(SchoolFacultyDepartment)
    school_id_number = models.CharField(max_length=10)
    course = models.ForeignKey(StudentCourseInformation, on_delete=models.DO_NOTHING)
    status = models.IntegerField(default=0)
    units = models.ManyToManyField(CourseUnits, related_name='students')

    def __str__(self) -> str:
        return self.student_name
    
    class Meta:
        db_table = 'student'



class StudentActivationOtp(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    is_validated = models.IntegerField(default=0)

    class Meta:
        db_table = 'student_activation_otp'

    def __str__(self):
        return self.email
    


    

# Enrollment Management
# Grading and Assessment
# Attendance Tracking
# Communication and Notifications
# Resources and Materials