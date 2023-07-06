from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from portal_authentication.models import LoginOtp, PasswordResetOtp

from portal_authentication.serializers import AdminForgotPasswordSerializer, AdminLoginSerializer, AdminNewPasswordSerializer, AdminResendOtpSerializer, VerifyLoginSerializer, VerifyOtpForgotPasswordSerializer

import re
import random

from utils.email_service import login_otp_email, password_resend_reset_otp_email, password_reset_otp_email
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
                    'message': 'Invalid data provided.',
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
            print('password', user.password)

            allowed_roles = ['admin']

            if not user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'user with this role {user.role.short_name} not allowed to access this portal',
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

            #Save otp to table
            if not LoginOtp.objects.create(email=username, otp=otp_code):
                return Response({
                    'status': False,
                    'message': 'Error saving otp to database'
                }, status=status.HTTP_400_BAD_REQUEST)

            #send email here
            if not login_otp_email(email=username, otp=otp_code):
                return Response({
                    'status': False,
                    'message': 'Error sending email'
                }, status=status.HTTP_400_BAD_REQUEST)

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
        
class VerifyLoginAPIView(APIView):
    serializer_class = VerifyLoginSerializer

    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided.',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            username = request.data.get('username')
            otp = request.data.get('otp')

            otp = int(otp)

            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, username)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=username)

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
                    'message': f'user with this role {user.role.short_name} not allowed to access this portal',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            login_otp = LoginOtp.objects.filter(email=username)

            if not login_otp.exists():
                return Response({
                    'status': False,
                    'message': 'otp with this email does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            login_otp = login_otp.last()
            print(type(login_otp.otp))
            print(type(otp))
            if login_otp.otp != otp:
                return Response({
                    'status': False,
                    'message': 'otp mismatch'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if login_otp.is_validated == 1:
                return Response({
                    'status': False,
                    'message': 'otp already validated'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            login_otp.is_validated=1
            login_otp.save()

            print("otp validated")

            refresh = RefreshToken.for_user(user)

            return Response({
                'status': True,
                'message': 'Logged in successfully',
                'access_token': str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)

            return Response({
                'status': False,
                'message': 'Could not log you in'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminForgotPasswordAPIView(APIView):
    serializer_class = AdminForgotPasswordSerializer

    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided.',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email = request.data.get('email')

            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=email)

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
                    'message': f'user with this role {user.role.short_name} not allowed to access this portal',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            otp_code = random.randint(111111, 999999)

            #Save otp to table
            if not PasswordResetOtp.objects.create(email=email, otp=otp_code):
                return Response({
                    'status': False,
                    'message': 'Error saving otp to database'
                }, status=status.HTTP_400_BAD_REQUEST)

            #send email here
            if not password_reset_otp_email(email=email, otp=otp_code):
                return Response({
                    'status': False,
                    'message': 'Error sending email'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                    'status': False,
                    'message': 'Passoword reset OTP sent via email please check to complete request.'
                }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not Iniatiate password reset'
            }, status=status.HTTP_400_BAD_REQUEST)
        

class VerifyOtpForgotPasswordAPIView(APIView):
    serializer_class = VerifyOtpForgotPasswordSerializer

    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided.',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email = request.data.get('email')
            otp = request.data.get('otp')

            otp = int(otp)

            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=email)

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
                    'message': f'user with this role {user.role.short_name} not allowed to access this portal',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            password_reset_otp = PasswordResetOtp.objects.filter(email=email)

            if not password_reset_otp.exists():
                return Response({
                    'status': False,
                    'message': 'otp with this email does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            password_reset_otp = password_reset_otp.last()
            print(type(password_reset_otp.otp))
            print(type(otp))
            if password_reset_otp.otp != otp:
                return Response({
                    'status': False,
                    'message': 'otp mismatch'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if password_reset_otp.is_validated == 1:
                return Response({
                    'status': False,
                    'message': 'otp already validated'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            password_reset_otp.is_validated=1
            password_reset_otp.save()

            print("otp validated")


            return Response({
                'status': True,
                'message': 'Otp verified..navigate to reset password'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)

            return Response({
                'status': False,
                'message': 'Could not log you in'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminNewPasswordAPIView(APIView):
    serializer_class = AdminNewPasswordSerializer

    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided.',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email = request.data.get('email')
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            confirm_new_password = request.data.get('confirm_new_password')



            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=email)

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
                    'message': f'user with this role {user.role.short_name} not allowed to access this portal',
                }, status=status.HTTP_400_BAD_REQUEST)

            password_match = user.check_password(old_password)
            
            print('password_match: ', password_match)
            if not password_match:
                return Response({
                    'status': False,
                    'message': 'Incorrect old password'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if new_password != confirm_new_password:
                return Response({
                    'status': False,
                    'message': 'new password and confirm passoword mismatch'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if old_password == new_password:
                return Response({
                    'status': False,
                    'message': 'Bad Request. No password reuse'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if len(new_password) < 5:
                return Response({
                    "status": False,
                    "message": "Password should be atleast 5 characters"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)

            user.save()

            print("password set successfully")

            return Response({
                'status': True,
                'message': 'Passoword change successful.'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not set up new password!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminResendOtpAPIView(APIView):
    serializer_class = AdminResendOtpSerializer

    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided.',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email = request.data.get('email')

            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=email)

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
                    'message': f'user with this role {user.role.short_name} not allowed to access this portal',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            otp_code = random.randint(111111, 999999)

            last_otp = PasswordResetOtp.objects.filter(email=email).last()

            last_otp.is_validated=1
            last_otp.save()

            #Save otp to table
            if not PasswordResetOtp.objects.create(email=email, otp=otp_code):
                return Response({
                    'status': False,
                    'message': 'Error saving otp to database'
                }, status=status.HTTP_400_BAD_REQUEST)

            #send email here
            if not password_resend_reset_otp_email(email=email, otp=otp_code):
                return Response({
                    'status': False,
                    'message': 'Error sending email'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                    'status': False,
                    'message': 'password resend otp successful'
                }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not Iniatiate password reset'
            }, status=status.HTTP_400_BAD_REQUEST)