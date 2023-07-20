from rest_framework import serializers

from portal_schools_api.models import FacultySchool


class AdminCreateSchoolSerializer(serializers.Serializer):
    school_name = serializers.CharField()
    school_dean = serializers.CharField()
    school_description = serializers.CharField()

class AdminActivateSchoolSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    school_code = serializers.CharField()
    school_name = serializers.CharField()

class AdminDeactivateSchoolSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    school_code = serializers.CharField()
    school_name = serializers.CharField()

class AdminDeleteSchoolSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    school_code = serializers.CharField()
    school_name = serializers.CharField()

class AdminViewDetailSchoolSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    school_code = serializers.CharField()
    school_name = serializers.CharField()

class AdminViewSchoolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=FacultySchool
        fields = '__all__'

class AdminCreateCourseSerializer(serializers.Serializer):
    course_name = serializers.CharField()
    course_description = serializers.CharField()
    course_duration = serializers.CharField()
    course_instructor = serializers.CharField()