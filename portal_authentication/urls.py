from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.AdminLoginAPIView.as_view(), name='admin-login-api'),
    path('verify-login/', views.VerifyLoginAPIView.as_view(), name='verify-login-api'),
]