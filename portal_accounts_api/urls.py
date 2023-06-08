from django.urls import path
from . import views

urlpatterns = [
    path("admin-create-accounts/", views.AdminCreateAccountsAPIView.as_view(), name='admin-create-school-department-api'),
]