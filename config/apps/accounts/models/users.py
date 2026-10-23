from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager as BaseUserManager, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError(_('Email is required.'))
        elif not username:
            raise ValueError(_('Username is required.'))

        if email == settings.DELETED_USER_EMAIL:
            raise ValueError(_('This email is reserved.'))
        elif username == settings.DELETED_USER_USERNAME:
            raise ValueError(_('This username is reserved.'))

        email = self.normalize_email(email)
        user_obj = self.model(email=email, username=username, **extra_fields)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_verified', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_verified') is not True:
            raise ValueError(_('Superuser must have is_verified=True'))
        return self.create_user(
            email=email, username=username, password=password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email
