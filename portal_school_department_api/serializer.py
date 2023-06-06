from rest_framework import serializers

class AdminCreateSchoolDepartmentSerializer(serializers.Serializer):
    school_name = serializers.CharField()
    department_name = serializers.CharField()
    department_description = serializers.CharField()
    department_chairman = serializers.CharField()
    admin_email = serializers.EmailField()
    