from django.db import models
from django.forms import CharField, EmailField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
from django.contrib.auth.models import UserManager
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your models here.

class User(AbstractBaseUser):
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'user'   


    @classmethod
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self(email=email)
        user.set_password(password)
        user.save()
        return user
