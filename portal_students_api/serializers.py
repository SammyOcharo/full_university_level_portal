from rest_framework import serializers
from portal_school_department_api.models import SchoolFacultyDepartment
from portal_schools_api.models import FacultySchool

from portal_students_api.models import Student

class AdminCreateStudentStudentSErializer(serializers.Serializer):
    school_code = serializers.CharField()
    department_code = serializers.CharField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    id_number = serializers.IntegerField()
    full_name = serializers.CharField()
    school_id_number = serializers.CharField()
    course = serializers.CharField()

class AdminActivateStudentSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    student_id = serializers.CharField()
    school_code = serializers.CharField()
    otp = serializers.IntegerField()

class AdminSuspendStudentSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    student_id = serializers.CharField()
    school_code = serializers.CharField()

class AdminDeactivateStudentSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    student_id = serializers.CharField()
    school_code = serializers.CharField()


class AdminViewDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFacultyDepartment
        fields = '__all__'


class AdminViewSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultySchool
        fields = '__all__'

class AdminViewAllStudentsSerializer(serializers.ModelSerializer):
    school = AdminViewSchoolSerializer()
    # department = AdminViewDepartmentSerializer()
    class Meta:
        model = Student
        fields = '__all__'

