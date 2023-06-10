from rest_framework import serializers

class AdminCreateStudentStudentSErializer(serializers.Serializer):
    school_code = serializers.CharField()
    department_code = serializers.CharField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    id_number = serializers.IntegerField()
    full_name = serializers.CharField()
    school_id_number = serializers.CharField()
    course = serializers.CharField()