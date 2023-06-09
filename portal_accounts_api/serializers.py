from rest_framework import serializers

class AdminCreateAccountsSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    accounts_email = serializers.CharField()
    accounts_name = serializers.CharField()
    accounts_Id = serializers.CharField()
