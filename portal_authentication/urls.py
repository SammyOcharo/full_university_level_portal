from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.AdminLoginAPIView.as_view(), name='admin-login-api')
]