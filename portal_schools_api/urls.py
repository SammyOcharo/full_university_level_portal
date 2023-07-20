from django.urls import path
from . import views

urlpatterns = [
    path('admin-create-school/', views.AdminCreateSchoolAPIView.as_view(), name='admin-create-school-api'),
    path('admin-activate-school/', views.AdminActivateSchoolAPIView.as_view(), name='admin-create-school-api'),
    path('admin-deactivate-school/', views.AdminDeactivateSchoolAPIView.as_view(), name='admin-deactivate-school-api'),
    path('admin-delete-school/', views.AdminDeleteSchoolAPIView.as_view(), name='admin-delete-school-api'),

    path('admin-view-school/', views.AdminViewSchoolAPIView.as_view(), name='admin-view-school-api'),


    #-------Course endpoints----------
    path('admin-create-course/', views.AdminCreateCourseAPIView.as_view(), name='admin-create-school-course-api')
]