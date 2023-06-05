from rest_framework import serializers


class AdminCreateSchoolSerializer(serializers.Serializer):
    school_name = serializers.CharField()
    school_dean = serializers.CharField()
    school_description = serializers.CharField()

class AdminDeactivateSchoolSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    school_code = serializers.CharField()
    school_name = serializers.CharField()