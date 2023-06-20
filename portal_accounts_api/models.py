from django.db import models
from django.contrib.auth import get_user_model

from portal_students_api.models import Student
from .choices import transaction_type

from portal_students_api.models import Student
User = get_user_model()

class StudentsFeePayments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    fee_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=60)
    payment_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'students_fee_table'
        verbose_name_plural = 'students_fee_table'

    def __str__(self) -> str:
        return self.student.student_name
    
class TransactionsMade(models.Model):
    transaction_type = models.CharField(max_length=50, choices=transaction_type, null=False)
    transaction_amount = models.DecimalField(max_digits=7, decimal_places=2)
    transacting_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    transaction_date = models.DateField()

    class Meta:
        db_table = 'Transactions'
        verbose_name_plural = 'Transactions'

    def __str__(self) -> str:
        return self.transacting_user.full_name
    
class InvoiceTable(models.Model):
    invoice_number = models.CharField(max_length=20)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    due_date = models.DateField()

    class Meta:
        db_table = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self) -> str:
        return self.student.student_name
