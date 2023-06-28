from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from portal_it.serializers import AdminApproveITAdminSerializer, AdminCreateITAdminSerializer, AdminDeactivateITAdminSerializer, AdminDeleteITAdminSerializer, AdminReactivateITAdminSerializer, AdminSuspendITAdminSerializer


class AdminCreateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))

class AdminApproveITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminApproveITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))


class AdminSuspendITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSuspendITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))


class AdminDeactivateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeactivateITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))


class AdminReactivateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminReactivateITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))



class AdminDeleteITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeleteITAdminSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid data provided!',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))
