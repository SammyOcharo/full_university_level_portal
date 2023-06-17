from django.urls import path
from . import views

urlpatterns = [
    path('admin-create-library-admin/', views.AdminCreateLibraryAdminAPIView.as_view(), name='admin-create-library-admin-api'),
    path('admin-activate-library-admin/', views.AdminCreateLibraryAdminAPIView.as_view(), name='admin-create-library-admin-api'),
]