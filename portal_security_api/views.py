import re
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from portal_security_api.models import Roles, SecurityDetails
from portal_security_api.security_exceptions import CustomExceptions
from utils.create_security_id import create_security_id

User = get_user_model()

from portal_security_api.serializers import AdminCreateSecurityAdminSerializer

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

            role = Roles.objects.filter(short_name=role)

            if not role.exists():
                return Response({
                    'status': False,
                    'message': 'Role does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            role = role.first()

            #function to create id of security
            security_id = create_security_id(first_name)
            SecurityDetails.objects.create(employee_id=security_id, role=role, first_name=first_name, last_name=last_name, employee_photo=employee_photo)
           

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
    pass