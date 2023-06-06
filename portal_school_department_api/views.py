from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import uuid
import re
from portal_school_department_api.models import SchoolFacultyDepartment

from portal_school_department_api.serializer import AdminCreateSchoolDepartmentSerializer
from portal_schools_api.models import FacultySchool

User = get_user_model()
# Create your views here.

class AdminCreateSchoolDepartmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateSchoolDepartmentSerializer

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
            
            school_name = request.data.get('school_name')
            department_name = request.data.get('department_name')
            department_description = request.data.get('department_description')
            department_chairman = request.data.get('department_chairman')
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

            school_name = school_name.lower()
            
            faculty_school = FacultySchool.objects.filter(school_name=school_name)

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