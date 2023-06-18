from rest_framework import serializers

class AdminCreateLibraryAdminSerializer(serializers.Serializer):
    library_admin_email = serializers.EmailField()
    id_number = serializers.CharField()
    mobile_number = serializers.CharField()
    school_id_number = serializers.CharField()
    full_name = serializers.CharField()

class AdminActivateLibraryAdminSerializer(serializers.Serializer):
    library_admin_email = serializers.EmailField()


class AddBooksSerializer(serializers.Serializer):
    book_name = serializers.CharField()
    book_category = serializers.CharField()
    