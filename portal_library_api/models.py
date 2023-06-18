from django.db import models


from django.contrib.auth import get_user_model

User = get_user_model()

class LibraryAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    id_number = models.CharField(max_length=12)
    mobile_number = models.CharField(max_length=15)
    school_id_number = models.CharField(max_length=15)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'library_admin'
        verbose_name_plural = 'lbrary_admins'

    def __str__(self) -> str:
        return self.email

class LibraryAdminActivationOtp(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    is_validated = models.IntegerField(default=0)

    class Meta:
        db_table = 'library_admin_activation_otp'

    def __str__(self):
        return self.email
    

class LibraryBooks(models.Model):
    book_name = models.CharField(max_length=30)
    book_category = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.book_name