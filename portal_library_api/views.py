from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from portal_library_api.serializers import AdminCreateLibraryAdminSerializer

# Create your views here.

class AdminCreateLibraryAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateLibraryAdminSerializer

    def post(self, request):
        try:
            data = request.data

            

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'Could not add librarry admin'
            }, status=status.HTTP_400_BAD_REQUEST)