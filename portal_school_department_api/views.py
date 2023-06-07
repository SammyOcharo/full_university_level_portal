import random
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import uuid
import re
from portal_school_department_api.models import DepartmentActivationOtp, SchoolFacultyDepartment

from portal_school_department_api.serializer import AdminActivateDepartmentSerializer, AdminCreateSchoolDepartmentSerializer
from portal_schools_api.models import FacultySchool
from utils.email_service import admin_department_otp_activate

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
        
class AdminActivateSchoolDepartmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminActivateDepartmentSerializer

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
            
            department_name = request.data.get('department_name')
            admin_email = request.data.get('admin_email')
            school_code = request.data.get('school_code')
            department_code = request.data.get('department_code')
            otp = request.data.get('otp')


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
            
            school = FacultySchool.objects.filter(school_code=school_code)

            if not school.exists():
                return Response({
                    'status': False,
                    'message': f'school does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            school = school.first()
            school_name = school.school_name

            if  school.status == 2:
                return Response({
                    'status': False,
                    'message': f'{school_name} is deactivated you need to reactivate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            school_department = SchoolFacultyDepartment.objects.filter(department_name=department_name, department_code=department_code)

            if not school_department.exists():
                return Response({
                    'status': False,
                    'message': f'{department_name} department does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            school_department=school_department.first()

            if  school_department.status == 2:
                return Response({
                    'status': False,
                    'message': f'{department_name} is deactivated you need to reactivate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if  school_department.status == 1:
                return Response({
                    'status': False,
                    'message': f'{department_name} is already activate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            db_saved_otp = DepartmentActivationOtp.objects.filter(email=admin_email)

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

            
            school_department.status=1
            school_department.save()
            print("Department activated!")

            return Response({
                'status': True,
                'message': f'{department_name} department Activated!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not activate department!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminDeactivateSchoolDepartmentAPIView(APIView):
    pass