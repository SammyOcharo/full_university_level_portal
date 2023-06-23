from rest_framework import serializers

class AdminCreateSecurityAdminSerializer(serializers.Serializer):
    role = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    employee_photo = serializers.ImageField()