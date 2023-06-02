
from rest_framework import serializers

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )