from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from backend.managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(_('user name'), max_length=50, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=50, unique=True)
    mobile_no = models.CharField(_('mobile number'), max_length=10, null=True)
    date_of_birth = models.DateField(_("date of birth"), null=True)
    creation_date = models.DateField(default=timezone.now)
    updation_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(_('is active'), default=True)
    student_id = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name


class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    status = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_created=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Authors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'authors'


class Books(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    isbn_number = models.CharField(max_length=30, unique=True)
    price = models.FloatField()
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, null=True)
    author = models.ForeignKey(Authors, on_delete=models.DO_NOTHING, null=True)
    regsi_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now_add=True)
    is_issued = models.BooleanField(default=False)
    image = models.ImageField(upload_to='books')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'books'

class IssuseNewBooks(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, limit_choices_to={'is_staff': False})
    books = models.ForeignKey(Books, on_delete=models.DO_NOTHING)
    is_returned = models.BooleanField(default=False)
    issue_date = models.DateTimeField(auto_now_add=True, blank=True)
    return_date = models.DateTimeField(auto_now=True, blank=True)
    fine = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.student}\t{self.is_returned}"
    class Meta:
        db_table = "issue_books"

@receiver(post_save, sender=IssuseNewBooks)
def update_books_issued_status(sender, instance, **kwargs):
    if instance.is_returned:
        instance.books.is_issued = False
        instance.return_date = timezone.now()
    else:
        instance.books.is_issued = True
    instance.books.save()

