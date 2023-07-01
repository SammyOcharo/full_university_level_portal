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
    pass

class AdminReactivateITAdminSerializer(serializers.Serializer):
    pass

class AdminDeleteITAdminSerializer(serializers.Serializer):
    pass