import random
import re
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from utils.email_service import admin_student_otp_activate, student_password_details
from utils.student_password import get_student_password
User = get_user_model()
from portal_authentication.models import Roles
from portal_school_department_api.models import SchoolFacultyDepartment
from portal_schools_api.models import FacultySchool
from portal_students_api.models import Student, StudentActivationOtp

from portal_students_api.serializers import AdminActivateStudentSerializer, AdminCreateStudentStudentSErializer, AdminDeactivateStudentSerializer, AdminSuspendStudentSerializer, AdminViewAllStudentsSerializer
# Create your views here.

class AdminCreateStudent(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateStudentStudentSErializer

    def post(self, request):
        try:
            data = request.data
            current_user = request.user
            print("current_user: ", current_user)
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            school_code = request.data.get('school_code')
            admin_email = request.data.get('admin_email')
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

            if User.objects.filter(email=email).exists():
                return Response({
                    'status': False,
                    'message': 'email already registered!'
                }, status=status.HTTP_400_BAD_REQUEST)

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

            password = get_student_password(full_name)

            user = User(email=email, mobile_number=mobile_number, id_number=id_number, username=email, role=role, full_name=full_name, password=password)

            user.save()
            
            student = Student.objects.create(user=user, student_name=full_name,national_id_number=id_number,  school=faculty_school_first, school_id_number=school_id_number, course=course)
            student.department.add(school_department.first().id)
            if not student:
                return Response({
                    'status': False,
                    'message': 'error saving student to database'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            otp = random.randint(111111,999999)

            if not StudentActivationOtp.objects.create(email=email, otp=otp):
                return Response({
                    'status': False,
                    'message': f'error saving otp to db!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not admin_student_otp_activate(email=current_user, otp=otp, student_name=full_name):
                return Response({
                    'status': False,
                    'message': f'error sending email'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            #send email with creds to the student
            if not student_password_details(email=email, password=password):
                return Response({
                    'status': False,
                    'message': f'error sending email to student'
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

            if  school.status == 2:
                return Response({
                    'status': False,
                    'message': f'school is deactivated you need to reactivate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            student_queryset = Student.objects.filter(school_id_number=student_id)

            if not student_queryset.exists():
                return Response({
                    'status': False,
                    'message': f'student not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            student=student_queryset.first()

            if  student.status == 2:
                return Response({
                    'status': False,
                    'message': f'{student.student_name} portal is deactivated you need to reactivate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if  student.status == 1:
                return Response({
                    'status': False,
                    'message': f'{student.student_name} portal is already activate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            db_saved_otp = StudentActivationOtp.objects.filter(email=student.user.email)

            if not db_saved_otp.exists():
                return Response({
                    'status': False,
                    'message': f'otp does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            
            
            db_saved_otp = db_saved_otp.last()

            if db_saved_otp.is_validated ==1:
                return Response({
                    'status': False,
                    'message': 'Otp already used!'
                }, status=status.HTTP_400_BAD_REQUEST)

            print(db_saved_otp.otp)
            print(otp)


            if db_saved_otp.otp != otp:
                return Response({
                    'status': False,
                    'message': 'Otp mismatch, check and try again'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            db_saved_otp.is_validated=1
            db_saved_otp.save()

       
            student.status = 1
            student.save()
            db_saved_otp.is_validated=1
            db_saved_otp.save()

            print("student activated!")

            return Response({
                'status': True,
                'message': f'student {student.student_name} Activated!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not activate student'
            }, status=status.HTTP_400_BAD_REQUEST)


class AdminSuspendStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSuspendStudentSerializer

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
            
            student_queryset = Student.objects.filter(school_id_number=student_id)

            if not student_queryset.exists():
                return Response({
                    'status': False,
                    'message': f'student not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            student=student_queryset.first()

            if  student.status == 2:
                return Response({
                    'status': False,
                    'message': f'{student.student_name} portal is deactivated you cannot suspend a deactivated account'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if  student.status == 3:
                return Response({
                    'status': False,
                    'message': f'{student.student_name} portal is already suspended.'
                }, status=status.HTTP_400_BAD_REQUEST)
            

       
            student.status = 3
            student.save()

            print("student suspended!")

            return Response({
                'status': True,
                'message': f'student {student.student_name} Suspended!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not suspended student'
            }, status=status.HTTP_400_BAD_REQUEST)
        

class AdminDeactivateStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeactivateStudentSerializer

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
                    'message': f'school is deactivated.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            student_queryset = Student.objects.filter(school_id_number=student_id)

            if not student_queryset.exists():
                return Response({
                    'status': False,
                    'message': f'student not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            student=student_queryset.first()

            if  student.status == 2:
                return Response({
                    'status': False,
                    'message': f'{student.student_name} portal is already deactivated.'
                }, status=status.HTTP_400_BAD_REQUEST)

   
            
       
            student.status = 2
            student.save()

            print("student deactivated!")

            return Response({
                'status': True,
                'message': f'student {student.student_name} Deactivated!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not deactivate student'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminViewAllStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminViewAllStudentsSerializer

    def get(self, request):
        try:
            current_user = request.user
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=current_user)

            print(user)

            if not user.exists():
                return Response({
                    'status': False,
                    'message': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            student = Student.objects.order_by('-id')

            serializer = self.serializer_class(student, many=True)

            return Response({
                'status': True,
                'list_students': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not return list of students!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminSearchStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminViewAllStudentsSerializer

    def get(self, request):
        try:
            current_user = request.user
            allowed_roles = ['admin']

            if not current_user.role.short_name in allowed_roles:
                return Response({
                    'status': False,
                    'message': f'role {current_user.role.short_name} not allowed to access this resource!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=current_user)

            print(user)

            if not user.exists():
                return Response({
                    'status': False,
                    'message': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            student_id = request.query_params.get('student_id')
            student = Student.objects.filter(school_id_number=student_id)

            if not student.exists():
                return Response({
                    'status': False,
                    'message': 'student not found!'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(student, many=True)

            return Response({
                'status': True,
                'list_students': serializer.data
            }, status=status.HTTP_200_OK)



        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not retrive student details!'
            }, status=status.HTTP_400_BAD_REQUEST)