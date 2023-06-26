import random
import re
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from portal_security_api.models import Roles, SecurityAdminActivationOtp, SecurityDetails
from portal_security_api.security_exceptions import CustomExceptions
from utils.create_security_id import create_security_id
from utils.email_service import admin_security_admin_creation_email

User = get_user_model()

from portal_security_api.serializers import AdminApproveSecuritySerializer, AdminCreateSecurityAdminSerializer, AdminSuspendSecurityAdminSerializer

class AdminCreateSecurityAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateSecurityAdminSerializer


    def post(self, request):
        try:
            
            current_user = request.user
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            print(current_user)
            
            user = User.objects.filter(email=current_user)

            print(user)

            if not user.exists():
                return Response({
                    'status': False,
                    'message': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            role = request.data.get('role')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            employee_photo = request.data.get('employee_photo')
            email = request.data.get('email')

            role = Roles.objects.filter(short_name=role)

            if not role.exists():
                return Response({
                    'status': False,
                    'message': 'Role does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            role = role.first()

            #function to create id of security
            security_id = create_security_id(first_name)
            SecurityDetails.objects.create(employee_id=security_id, role=role, email=email, first_name=first_name, last_name=last_name, employee_photo=employee_photo)

            otp = random.randint(111111, 999999)
            SecurityAdminActivationOtp.objects.create(email=email, otp=otp)

            #send email
            admin_security_admin_creation_email(email=current_user, otp=otp, security_admin_email=email)

            return Response({
                'status': True,
                'message': 'Security admin added successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Error creating security admin!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminApproveSecurityAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminApproveSecuritySerializer


    def post(self, request):
        try:
            current_user = request.user
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            print(current_user)
            
            user = User.objects.filter(email=current_user)

            print(user)

            if not user.exists():
                return Response({
                    'status': False,
                    'message': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            email = request.data.get('email')
            otp = request.data.get('otp')

            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(email)
            
            security_user = SecurityDetails.objects.filter(email=email)

            print(security_user)

            if not security_user.exists():
                return Response({
                    'status': False,
                    'message': 'security admin does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            security_user = security_user.first()

            if  security_user.status == 2:
                return Response({
                    'status': False,
                    'message': f'security admin{security_user.first_name} is deactivated you need to reactivate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            

            db_saved_otp = SecurityAdminActivationOtp.objects.filter(email=email)

            if not db_saved_otp.exists():
                return Response({
                    'status': False,
                    'message': f'otp does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            db_saved_otp = db_saved_otp.last()

            print(db_saved_otp.otp)
            print(otp)


            if db_saved_otp.otp != otp:
                return Response({
                    'status': False,
                    'message': 'Otp mismatch, check and try again'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            db_saved_otp.is_validated=1
            db_saved_otp.save()

            
            security_user.status=1
            security_user.save()
            print("security admin activated!")

            return Response({
                'status': True,
                'message': f' security admin with first name {security_user.first_name} and email {security_user.email} is Activated!'
            }, status=status.HTTP_200_OK)


        except Exception as e:
            print(str(e))
            return Response({
                'status': False,
                'message': 'Could not approve security admin.'
            }, status=status.HTTP_200_OK)
        
class AdminSuspendSecurityAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSuspendSecurityAdminSerializer 

    def post(self, request):
        try:

            current_user = request.user
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email = request.data.get('email')


            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            security_admin = SecurityDetails.objects.filter(email=email)

            if not security_admin.exists():
                return Response({
                    'status': False,
                    'message': ' security admin does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            security_admin=security_admin.first()

            if  security_admin.status == 2:
                return Response({
                    'status': False,
                    'message': f'security admin with first name {security_admin} is already suspended.'
                }, status=status.HTTP_400_BAD_REQUEST)
            

            security_admin.status = 2
            security_admin.save()

            print("security admin suspended successfully")
            return Response({
                'status': True,
                'message': 'Security admin suspended!'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'status': False,
                'message': 'unable to suspend security admin!'
            }, status=status.HTTP_400_BAD_REQUEST)


class AdminDeactivateSecurityAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSuspendSecurityAdminSerializer 

    def post(self, request):
        try:

            current_user = request.user
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email = request.data.get('email')


            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            security_admin = SecurityDetails.objects.filter(email=email)

            if not security_admin.exists():
                return Response({
                    'status': False,
                    'message': ' security admin does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            security_admin=security_admin.first()

            if  security_admin.status == 3:
                return Response({
                    'status': False,
                    'message': f'security admin with first name {security_admin} is already deactivated.'
                }, status=status.HTTP_400_BAD_REQUEST)
            

            security_admin.status = 3
            security_admin.save()

            print("security admin deactivated successfully")
            return Response({
                'status': True,
                'message': 'Security admin deactivated!'
            }, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({
                'status': False,
                'message': 'unable to deactivate security admin!'
            }, status=status.HTTP_400_BAD_REQUEST)

class AdminReactivateSecurityAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSuspendSecurityAdminSerializer 

    def post(self, request):
        try:

            current_user = request.user
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email = request.data.get('email')


            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            security_admin = SecurityDetails.objects.filter(email=email)

            if not security_admin.exists():
                return Response({
                    'status': False,
                    'message': ' security admin does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            security_admin=security_admin.first()

            if  security_admin.status == 1:
                return Response({
                    'status': False,
                    'message': f'security admin with first name {security_admin} is already reactivated.'
                }, status=status.HTTP_400_BAD_REQUEST)
            

            security_admin.status = 1
            security_admin.save()

            print("security admin reactivated successfully")
            return Response({
                'status': True,
                'message': 'Security admin reactivated!'
            }, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({
                'status': False,
                'message': 'unable to reactivate security admin!'
            }, status=status.HTTP_400_BAD_REQUEST)