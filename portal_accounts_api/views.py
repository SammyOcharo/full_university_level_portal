from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import re
import uuid
import random
from portal_accounts_api.models import UniversityAccounts

from portal_accounts_api.serializers import AdminCreateAccountsSerializer
# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()

class AdminCreateAccountsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateAccountsSerializer

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
            
            accounts_admin_email = request.data.get('accounts_email')
            accounts_admin_name = request.data.get('accounts_name')
            accounts_admin_Id = request.data.get('accounts_Id')
            admin_email = request.data.get('admin_email')

            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            valid_email = re.fullmatch(email_regex, admin_email)

            if not valid_email:
                return Response({
                    'status': False,
                    'message': 'Invalid email provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(admin_email)
            
            user = User.objects.filter(email=admin_email)

            print(user)

            if not user.exists():
                return Response({
                    'status': False,
                    'message': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)

            
            
            faculty_school = UniversityAccounts.objects.filter(school_name=school_name)

            if not faculty_school.exists():
                return Response({
                    'status': False,
                    'message': f'school name {school_name} does exists!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            faculty_school = faculty_school.first()

            department_code= uuid.uuid4().hex


            if not SchoolFacultyDepartment.objects.create(department_code=department_code, school=faculty_school, department_name=department_name, department_description=department_description, department_chairman=department_chairman):
                return Response({
                    'status': False,
                    'message': f'error creating {department_name} department'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            otp = random.randint(111111, 999999)

            if not admin_department_otp_activate(email=admin_email, otp=otp, department_name=department_name):
                return Response({
                    'status': False,
                    'message': f'error sending email to {admin_email} '
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not DepartmentActivationOtp.objects.create(email=admin_email, otp=otp):
                return Response({
                    'status': False,
                    'message': f'error saving otp to db'
                }, status=status.HTTP_400_BAD_REQUEST)


            return Response({
                'status': True,
                'message': f'{department_name} department created successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'could not create the department for some reason!'
            }, status=status.HTTP_400_BAD_REQUEST)