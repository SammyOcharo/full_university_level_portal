from rest_framework import serializers

from portal_students_api.models import Student

class AdminCreateStudentStudentSErializer(serializers.Serializer):
    school_code = serializers.CharField()
    department_code = serializers.CharField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    id_number = serializers.IntegerField()
    full_name = serializers.CharField()
    school_id_number = serializers.CharField()
    course = serializers.CharField()

class AdminActivateStudentSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    student_id = serializers.CharField()
    school_code = serializers.CharField()
    otp = serializers.IntegerField()

class AdminSuspendStudentSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    student_id = serializers.CharField()
    school_code = serializers.CharField()

class AdminDeactivateStudentSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    student_id = serializers.CharField()
    school_code = serializers.CharField()

class AdminViewAllStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
