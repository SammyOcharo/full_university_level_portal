from django.urls import path
from . import views

urlpatterns = [
    path('admin-create-school/', views.AdminCreateSchoolAPIView.as_view(), name='admin-create-school-api'),
    path('admin-activate-school/', views.AdminActivateSchoolAPIView.as_view(), name='admin-create-school-api'),
    path('admin-deactivate-school/', views.AdminDeactivateSchoolAPIView.as_view(), name='admin-deactivate-school-api'),
]