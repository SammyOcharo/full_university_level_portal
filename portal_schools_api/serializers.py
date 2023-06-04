from rest_framework import serializers


class AdminCreateSchoolSerializer(serializers.Serializer):
    school_name = serializers.CharField()
    school_dean = serializers.CharField()
    school_description = serializers.CharField()