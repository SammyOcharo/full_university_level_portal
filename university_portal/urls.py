"""
URL configuration for university_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('apps/admin/vi/admin/', admin.site.urls),
    path('apps/admin/v1/authentication/', include('portal_authentication.urls')),
    path('apps/admin/v1/accounts/', include('portal_accounts_api.urls')),
    path('apps/admin/v1/admins/', include('portal_admin_api.urls')),
    path('apps/admin/v1/schools/', include('portal_schools_api.urls')),
    path('apps/admin/v1/students/', include('portal_students_api.urls')),
    path('apps/admin/v1/departments/', include('portal_school_department_api.urls')),
    path('apps/admin/v1/library/', include('portal_library_api.urls')),
    path('apps/admin/v1/security/', include('portal_security_api.urls')),
    path('apps/admin/v1/it/', include('portal_it.urls')),
]
