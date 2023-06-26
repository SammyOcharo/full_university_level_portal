from rest_framework import serializers

class AdminCreateSecurityAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    employee_photo = serializers.ImageField()


class AdminApproveSecuritySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

class AdminSuspendSecurityAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()

class AdminDeleteSecurityAdminSerializer(serializers.Serializer):
    id = serializers.IntegerField()