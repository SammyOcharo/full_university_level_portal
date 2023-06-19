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
    Title = serializers.CharField()
    Author = serializers.CharField()
    ISBN = serializers.CharField()
    Language = serializers.CharField()
    Description = serializers.CharField()
    Number_of_Pages = serializers.CharField()
    Location = serializers.CharField()
    Publisher = serializers.CharField()
    genre = serializers.CharField()
    Cover_Image = serializers.ImageField()
    Publication_Date = serializers.DateField()
    