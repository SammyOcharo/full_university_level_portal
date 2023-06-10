from django.urls import path
from . import views
urlpatterns = [
    path('admin-create-student/',views.AdminCreateStudent.as_view(), name='admin-create-student-api' )
]