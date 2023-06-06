from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()

import uuid
import re
from portal_schools_api.models import FacultySchool

from portal_schools_api.serializers import AdminActivateSchoolSerializer, AdminCreateSchoolSerializer, AdminDeactivateSchoolSerializer, AdminDeleteSchoolSerializer, AdminViewDetailSchoolSerializer, AdminViewSchoolSerializer


# Create your views here.

class AdminCreateSchoolAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateSchoolSerializer

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
            school_dean = request.data.get('school_dean')
            school_description = request.data.get('school_description')

            school_name = school_name.lower()

            if len(school_name) < 8:
                return Response({
                    'status': False,
                    'message': f'school name {school_name} too short!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            faculty_school = FacultySchool.objects.filter(school_name=school_name)

            if faculty_school.exists():
                return Response({
                    'status': False,
                    'message': f'school name {school_name} exists!'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            school_code = uuid.uuid4().hex
            
            if not FacultySchool.objects.create(school_code=school_code, school_name=school_name,school_dean=school_dean,  school_description=school_description):
                return Response({
                    'status': False,
                    'message': 'error saving schhol to database'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'status': True,
                'message': f'{school_name} created successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'could not create the school for some reason!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminActivateSchoolAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminActivateSchoolSerializer

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
            admin_email = request.data.get('admin_email')
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
            
            school = FacultySchool.objects.filter(school_code=school_code, school_name=school_name)

            if not school.exists():
                return Response({
                    'status': False,
                    'message': f'{school_name} does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            school = school.first()

            if  school.status == 2:
                return Response({
                    'status': False,
                    'message': f'{school_name} is deactivated you need to reactivate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if  school.status == 1:
                return Response({
                    'status': False,
                    'message': f'{school_name} is already activate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            school.status=1
            school.save()
            print("School Activated!")

            return Response({
                'status': True,
                'message': f'{school_name} Activated!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not deactivate schhol!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminDeactivateSchoolAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeactivateSchoolSerializer

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
            admin_email = request.data.get('admin_email')
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
            
            school = FacultySchool.objects.filter(school_code=school_code, school_name=school_name)

            if not school.exists():
                return Response({
                    'status': False,
                    'message': f'{school_name} does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            school = school.first()

            if  school.status == 2:
                return Response({
                    'status': False,
                    'message': f'{school_name} already deactivated'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            school.status=2
            school.save()
            print("School deactivated!")

            return Response({
                'status': True,
                'message': f'{school_name} deactivated!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not deactivate school!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminDeleteSchoolAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeleteSchoolSerializer

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
            admin_email = request.data.get('admin_email')
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
            
            school = FacultySchool.objects.filter(school_code=school_code, school_name=school_name)

            if not school.exists():
                return Response({
                    'status': False,
                    'message': f'{school_name} does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            school = school.first()
            school.delete()
            print("school deleted successfully!")

            return Response({
                'status': True,
                'message': f'{school_name} deleted!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not delete school!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminViewSchoolAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminViewDetailSchoolSerializer

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
            admin_email = request.data.get('admin_email')
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
            
            school = FacultySchool.objects.filter(school_code=school_code, school_name=school_name)

            serializer = AdminViewSchoolSerializer(school, many=True)

            return Response({
                'status': True,
                'message': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not view school!'
            }, status=status.HTTP_400_BAD_REQUEST)