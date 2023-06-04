from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid
from portal_schools_api.models import FacultySchool

from portal_schools_api.serializers import AdminCreateSchoolSerializer


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