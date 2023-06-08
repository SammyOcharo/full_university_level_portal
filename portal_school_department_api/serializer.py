from rest_framework import serializers

from portal_school_department_api.models import SchoolFacultyDepartment

class AdminCreateSchoolDepartmentSerializer(serializers.Serializer):
    school_name = serializers.CharField()
    department_name = serializers.CharField()
    department_description = serializers.CharField()
    department_chairman = serializers.CharField()
    admin_email = serializers.EmailField()
    

class AdminActivateDepartmentSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    school_code = serializers.CharField()
    department_code = serializers.CharField()
    department_name = serializers.CharField()
    otp = serializers.IntegerField()

class AdminDeactivateDepartmentSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    school_code = serializers.CharField()
    department_name = serializers.CharField()
    department_code = serializers.CharField()

class AdminDeleteSchoolDepartmentSerailizer(serializers.Serializer):
    admin_email = serializers.EmailField()
    school_code = serializers.CharField()
    department_name = serializers.CharField()
    department_code = serializers.CharField()

class AdminViewAllSchoolDepartmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolFacultyDepartment
        fields = '__all__'