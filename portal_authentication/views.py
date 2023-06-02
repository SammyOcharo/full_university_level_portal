from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from portal_authentication.serializers import AdminLoginSerializer

import re
import random
User = get_user_model()

class AdminLoginAPIView(APIView):
    serializer_class = AdminLoginSerializer

    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Inalid data provided.',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            username = request.data.get('username')
            password = request.data.get('password')

            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, username)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(username=username)

            if not user.exists():
                return Response({
                    'status': False,
                    'message': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            user = user.first()

            allowed_roles = ['admin']

            if not user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': 'User with this role not allowed to access this portal'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if user.status == 0:
                return Response({
                    'status': False,
                    'message': 'Admin not yet approved please contact IT.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if user.status == 2:
                return Response({
                    'status': False,
                    'message': 'Admin account is suspended check in with IT'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            auth_user = authenticate(username=username, password=password)

            if auth_user is None:
                return Response({
                    'status': False,
                    'message': 'Invalid credentials provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            otp_code = random.randint(111111, 999999)

            print(otp_code)

            #send email here

            return Response({
                    'status': False,
                    'message': 'Login OTP sent via email please check to complete login.'
                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)

            return Response({
                'status': False,
                'message': 'Login Unsuccessful. please contact admin/IT'
            }, status=status.HTTP_400_BAD_REQUEST)