from django.urls import path
from . import views

urlpatterns = [
    path("admin-create-school-department/", views.AdminCreateSchoolDepartmentAPIView.as_view(), name='admin-create-school-department-api')
]