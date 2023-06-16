from rest_framework import serializers

class AdminCreateLibraryAdminSerializer(serializers.Serializer):
    library_admin_email = serializers.EmailField()
    id_number = serializers.CharField()
    mobile_number = serializers.CharField()
    school_id_number = serializers.CharField()
    full_name = serializers.CharField()
