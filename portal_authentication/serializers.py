
from rest_framework import serializers

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

class VerifyLoginSerializer(serializers.Serializer):
   username = serializers.EmailField()
   otp = serializers.IntegerField()

class AdminForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpForgotPasswordSerializer(serializers.Serializer):
   email = serializers.EmailField()
   otp = serializers.IntegerField()

class AdminNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    new_password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    confirm_new_password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

class AdminResendOtpSerializer(serializers.Serializer):
   email = serializers.EmailField()