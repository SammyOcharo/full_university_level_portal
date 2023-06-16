import random
import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from portal_authentication.models import Roles
from portal_library_api.models import LibraryAdmin, LibraryAdminActivationOtp
from utils.email_service import admin_library_admin_creation_email

User = get_user_model()
from portal_library_api.serializers import AdminCreateLibraryAdminSerializer

# Create your views here.

class AdminCreateLibraryAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateLibraryAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            library_admin_email = request.data.get('library_admin_email')
            id_number = request.data.get('id_number')
            mobile_number = request.data.get('mobile_number')
            school_id_number = request.data.get('school_id_number')
            full_name = request.data.get('full_name')

            current_user = request.user
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            admin_user = User.objects.filter(email=current_user)

            print(admin_user)
            
            if not admin_user.exists():
                return Response({
                    'status': False,
                    'message': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, library_admin_email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            role = 'library'
            role = Roles.objects.filter(short_name=role).first()
            
            
            user = User.objects.create(email =library_admin_email, mobile_number = mobile_number, id_number = id_number,  username = library_admin_email, role = role, full_name = full_name)
            
            if not LibraryAdmin.objects.create(user=user, email=library_admin_email, id_number=id_number, mobile_number=mobile_number, school_id_number=school_id_number ):
                return Response({
                    'status': False,
                    'message': 'error saving library admin to database!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            #create otp for account activation
            otp = random.randint(111111, 999999)

            if not LibraryAdminActivationOtp(email=library_admin_email, otp=otp):
                return Response({
                    'status': False,
                    'message': 'error saving otp!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            #send mail
            admin_library_admin_creation_email(email=current_user, otp=otp, library_admin_email=library_admin_email)

            return Response({
                    'status': True,
                    'message': f'Admin with email {current_user} has sucessfully registered library admin with email {library_admin_email}'
                }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not add library admin'
            }, status=status.HTTP_400_BAD_REQUEST)