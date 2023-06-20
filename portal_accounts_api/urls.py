from django.urls import path
from . import views

urlpatterns = [
    path("admin-create-accounts/", views.AdminCreateAccountsAPIView.as_view(), name='admin-create-school-department-api'),
    path('admin-view-alltransactions/', views.AdminViewAllTransactionsAPIView.as_view(), name='admin-view-transactions-api'),
    path('admin-view-all-invoices/', views.AdminViewAllInvoicesAPIView.as_view(), name='admin-view-all-invoices-api'),
    path('admin-view-student_fees/', views.AdminViewStudentsFeeAPIView.as_view(), name='admin-view-students-fees-api')
]