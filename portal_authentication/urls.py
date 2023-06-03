from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.AdminLoginAPIView.as_view(), name='admin-login-api'),
    path('admin-verify-login/', views.VerifyLoginAPIView.as_view(), name='verify-login-api'),
    path('admin-forgot-password/', views.AdminForgotPasswordAPIView.as_view(), name='admin-forgot-password-api'),
    path('admin-verify-forgot-password/', views.VerifyOtpForgotPasswordAPIView.as_view(), name='admin-verify-forgot-password-api'),
    path('admin-new-password/', views.AdminNewPasswordAPIView.as_view(), name='admin-new-password-api'),
    path('admin-resend-forgot-password-otp/', views.AdminResendOtpAPIView.as_view(), name='resend-otp-api')
]