from django.urls import path
from . import views
urlpatterns = [
    path("admin-create-it-admin/", views.AdminCreateITAdminAPIView.as_view(), name='admin-create-it-admin-api'),
    path('admin-approve-it-admin/', views.AdminApproveITAdminAPIView.as_view(), name='admin-approve-it-admin-api'),
    path('admin-suspend-it-admin/', views.AdminSuspendITAdminAPIView.as_view(), name='admin-suspend-it-admin-api'),
    path('admin-deactivate-it-admin/', views.AdminDeactivateITAdminAPIView.as_view(), name='admin-deactivate-it-admin-api'),
    path('admin-reactivate-it-admin/', views.AdminReactivateITAdminAPIView.as_view(), name='admin-reactivate-it-admin-api'),
    path('admin-delete-it-admin/', views.AdminDeleteITAdminAPIView.as_view(), name='admin-delete-it-admin-api')
]