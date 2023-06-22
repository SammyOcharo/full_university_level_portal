from django.urls import path
from . import views
urlpatterns = [
    path("admin-create-security-admin/", views.AdminCreateSecurityAdminAPIView.as_view(), name='admin-create-security-admin-api')
]