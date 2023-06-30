import random
import re
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from portal_authentication.models import Roles
from portal_it.models import ITAdmin, ITAdminActivationOtp

from portal_it.serializers import AdminApproveITAdminSerializer, AdminCreateITAdminSerializer, AdminDeactivateITAdminSerializer, AdminDeleteITAdminSerializer, AdminReactivateITAdminSerializer, AdminSuspendITAdminSerializer
from utils.create_security_id import create_lib_id
from utils.email_service import it_admin_creation_email

User = get_user_model()

class AdminCreateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateITAdminSerializer

    def post(self, request):
        try:
            current_user = request.data
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
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            id_number = request.data.get('id_number')
            full_name = request.data.get('full_name')
            email = request.data.get('email')
            mobile_number = request.data.get('mobile_number')
            role = request.data.get('role')

            if len(id_number) < 8:
                return Response({
                    'status': False,
                    'message': 'ID number too short'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            user = User.objects.filter(email=email)

            if user.exists():
                return Response({
                    'status': False,
                    'message': 'User already exists!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            role = Roles.objects.filter(short_name=role)

            if not role.exists():
                return Response({
                    'status': False,
                    'message': 'Role provided does not exist!'
                }, status=status.HTTP_404_NOT_FOUND)
            
            role = role.first()
            
            user = User(
                email = email,
                mobile_number = mobile_number,
                id_number=id_number,
                username = email,
                role = role,
                full_name=full_name
            )
            user.save()
            
            school_id_number = create_lib_id(full_name)
            
            ITAdmin.objects.create(user=user, id_number=id_number, full_name=full_name, school_id_number=school_id_number, email=email)

            otp = random.randint(111111, 999999)

            if not ITAdminActivationOtp.objects.create(otp=otp, email=email):
                return Response({
                    'status': False,
                    'message': 'error saving otp to db'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            it_admin_creation_email(email=current_user, otp=otp, it_admin_email=email)

            return Response({
                'status': False,
                'message': 'Successfully created the IT admin!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            return Response({
                'status': False,
                'message': 'error creating IT admin!'
            }, status=status.HTTP_400_BAD_REQUEST)

class AdminApproveITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminApproveITAdminSerializer

    def post(self, request):
        try:
            current_user = request.user
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
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
            
            it_user = ITAdmin.objects.filter(email=email)

            print(it_user)

            if not it_user.exists():
                return Response({
                    'status': False,
                    'message': 'security admin does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            it_user = it_user.first()

            if  it_user.status == 2:
                return Response({
                    'status': False,
                    'message': f'security admin{it_user.full_name} is deactivated you need to reactivate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            

            db_saved_otp = ITAdminActivationOtp.objects.filter(email=email)

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

            
            it_user.status=1
            it_user.save()
            print("it admin activated!")

            return Response({
                'status': True,
                'message': f' it admin with first name {it_user.full_name} and email {it_user.email} is Activated!'
            }, status=status.HTTP_200_OK)


        except Exception as e:
            print(str(e))
            return Response({
                'status': False,
                'message': 'Could not approve security admin.'
            }, status=status.HTTP_400_BAD_REQUEST)


class AdminSuspendITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSuspendITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))


class AdminDeactivateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeactivateITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))


class AdminReactivateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminReactivateITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))



class AdminDeleteITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeleteITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))
