from django.urls import path
from . import views
urlpatterns = [
    path("admin-create-security-admin/", views.AdminCreateSecurityAdminAPIView.as_view(), name='admin-create-security-admin-api'),
    path('admin-approve-security-admin/', views.AdminApproveSecurityAdminAPIView.as_view(), name='admin-approve-security-admin-api'),
    path('admin-suspend-security-admin/', views.AdminSuspendSecurityAdminAPIView.as_view(), name='admin-suspend-security-admin-api'),
    path('admin-deactivate-security-admin/', views.AdminDeactivateSecurityAdminAPIView.as_view(), name='admin-deactivate-security-admin-api'),
    path('admin-reactivate-security-admin/', views.AdminReactivateSecurityAdminAPIView.as_view(), name='admin-reactivate-security-admin-api'),
    path('admin-delete-security-admin/', views.AdminDeleteSecurityAdminAPIView.as_view(), name='admin-delete-security-admin-api')
]