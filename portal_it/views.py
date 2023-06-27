from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from portal_it.serializers import AdminApproveITAdminSerializer, AdminCreateITAdminSerializer, AdminDeactivateITAdminSerializer, AdminDeleteITAdminSerializer, AdminReactivateITAdminSerializer, AdminSuspendITAdminSerializer


class AdminCreateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCreateITAdminSerializer

    def post(self, request):
        pass

class AdminApproveITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminApproveITAdminSerializer

    def post(self, request):
        pass


class AdminSuspendITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSuspendITAdminSerializer

    def post(self, request):
        pass


class AdminDeactivateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeactivateITAdminSerializer

    def post(self, request):
        pass


class AdminReactivateITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminReactivateITAdminSerializer

    def post(self, request):
        pass



class AdminDeleteITAdminAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminDeleteITAdminSerializer

    def post(self, request):
        pass
