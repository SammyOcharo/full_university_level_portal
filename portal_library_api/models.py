from django.db import models


from django.contrib.auth import get_user_model

from .books_genre import choices

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
    
class Genre(models.Model):
    name = models.CharField(max_length=50, choices=choices)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class LibraryBooks(models.Model):
    Title = models.CharField(max_length=30)
    Author = models.CharField(max_length=30)
    Publication_Date = models.DateField()
    ISBN = models.CharField(max_length=50)
    Description = models.TextField()
    Publisher = models.CharField(max_length=60)
    Genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    Language = models.CharField(max_length=60)
    Cover_Image = models.ImageField()
    Number_of_Pages = models.CharField(max_length=60)
    Availability = models.IntegerField(default=0)
    Location = models.CharField(max_length=60)
    Borrower = models.ForeignKey(User,max_length=60, null=True, on_delete=models.DO_NOTHING)
    Borrow_date = models.DateField(null=True)
    Due_Date = models.DateField(null=True)



    def __str__(self) -> str:
        return self.Title
    
    class Meta:
        verbose_name = 'library_books'
        verbose_name_plural = 'library_books'
        ordering = ['-id']
        db_table = 'library_books'


