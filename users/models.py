from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True,
                                    error_messages={'unique': "Email already exists"})
    phone_number = models.CharField(max_length=100, unique=True, null=True, blank=True,
                                    error_messages={'unique': "Mobile number already exists"})
    is_manager= models.BooleanField('Is manager', default=False)
    is_customer = models.BooleanField('Is customer', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    

    objects = UserManager()


    class Meta:
        db_table = 'user_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ["-id"]

    def __str__(self):
        return self.email


class OTPVerifier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)  # Temporary email storage
    otp = models.IntegerField()
    created_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):

        return str(self.otp)