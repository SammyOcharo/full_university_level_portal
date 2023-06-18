from django.urls import path
from . import views

urlpatterns = [
    path('admin-create-library-admin/', views.AdminCreateLibraryAdminAPIView.as_view(), name='admin-create-library-admin-api'),
    path('admin-activate-library-admin/', views.AdminActivateLibraryAdminAPIView.as_view(), name='admin-activate-library-admin-api'),
    path('admin-add-books/', views.AdminAddBooksAPIView.as_view(), name='admin-add-books-api')
]