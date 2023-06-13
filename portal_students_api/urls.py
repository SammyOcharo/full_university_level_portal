from django.urls import path
from . import views
urlpatterns = [
    path('admin-create-student/',views.AdminCreateStudent.as_view(), name='admin-create-student-api'),
    path('admin-activate-student/', views.AdminActivateStudentAPIView.as_view(), name='admin-activate-school-api'),
    path('admin-suspend-student/', views.AdminSuspendStudentAPIView.as_view(), name='admin-suspended-student'),
    path('admin-deactivate-student/', views.AdminDeactivateStudentAPIView.as_view(), name='admin-deactivate-student'),
]