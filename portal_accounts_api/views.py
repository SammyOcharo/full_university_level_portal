from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import re

from portal_accounts_api.serializers import AdminCreateAccountsSerializer

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

            
            

            return Response({
                'status': True,
                'message': f'department created successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))

            return Response({
                'status': False,
                'message': 'could not create the department for some reason!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AdminViewAllTransactionsAPIView(APIView):
    pass

class AdminViewAllInvoicesAPIView(APIView):
    pass

class AdminViewStudentsFeeAPIView(APIView):
    pass