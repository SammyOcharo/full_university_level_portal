import re
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
User = get_user_model()
from portal_authentication.models import Roles
from portal_school_department_api.models import SchoolFacultyDepartment
from portal_schools_api.models import FacultySchool
from portal_students_api.models import Student

from portal_students_api.serializers import AdminActivateStudentSerializer, AdminCreateStudentStudentSErializer
# Create your views here.

class AdminCreateStudent(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateStudentStudentSErializer

    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            school_code = request.data.get('school_code')
            department_code = request.data.get('department_code')
            email = request.data.get('email')
            mobile_number = request.data.get('mobile_number')
            id_number = request.data.get('id_number')
            full_name = request.data.get('full_name')
            school_id_number = request.data.get('school_id_number')
            course = request.data.get('course')
            
            faculty_school = FacultySchool.objects.filter(school_code=school_code)
            faculty_school_first = faculty_school.first()

            school_name = faculty_school.first().school_name

            if not faculty_school.exists():
                return Response({
                    'status': False,
                    'message': f'school name {school_name} does not exists!'
                }, status=status.HTTP_404_NOT_FOUND)
            
            school_department = SchoolFacultyDepartment.objects.filter(department_code=department_code)
            school_department_name = school_department.first().department_name

            if not school_department.exists():
                return Response({
                    'status': False,
                    'message': f'department name {school_department_name} does not exists!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            role = 'students'
            
            role = Roles.objects.filter(short_name=role)

            if not role.exists():
                return Response({
                    'status': False,
                    'message': f'role {role} does not exists!'
                }, status=status.HTTP_404_NOT_FOUND)
            
            role = role.first()

            user = User(email=email, mobile_number=mobile_number, id_number=id_number, username=email, role=role, full_name=full_name)

            user.save()
            
            student = Student.objects.create(user=user, student_name=full_name,national_id_number=id_number,  school=faculty_school_first, school_id_number=school_id_number, course=course)
            student.department.add(school_department.first().id)
            if not student:
                return Response({
                    'status': False,
                    'message': 'error saving student to database'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'status': True,
                'message': f'student {full_name} created successfully!'
            }, status=status.HTTP_200_OK)


        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not create student!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminActivateStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminActivateStudentSerializer

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
            
            admin_email = request.data.get('admin_email')
            student_id = request.data.get('student_id')
            school_code = request.data.get('school_code')

            

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

            if  school.status == 2:
                return Response({
                    'status': False,
                    'message': f'school is deactivated you need to reactivate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            student = Student.objects.filter(school_id_number=student_id)

            if not student.exists():
                return Response({
                    'status': False,
                    'message': f'student not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            student = student.first()
            student.status = 1
            student.save()

            print("student activated!")
            
            
            school.status=1
            school.save()
            print("School Activated!")

            return Response({
                'status': True,
                'message': f'student {student.student_name} Activated!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not deactivate schhol!'
            }, status=status.HTTP_400_BAD_REQUEST)
