from rest_framework import serializers

class AdminCreateITAdminSerializer(serializers.Serializer):
    id_number = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    role = serializers.CharField()

class AdminApproveITAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

class AdminSuspendITAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()

class AdminDeactivateITAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()

class AdminReactivateITAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AdminDeleteITAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()