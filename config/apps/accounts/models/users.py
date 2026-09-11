from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager as BaseUserManager, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email is required.'))
        if email == settings.DELETED_USER_EMAIL:
            raise ValueError(_('This email is reserved.'))
        email = self.normalize_email(email)
        user_obj = self.model(email=email, **extra_fields)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True'))
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def delete(self, *args, **kwargs):
        deleted_profile = self.get_deleted_user()
        self.profile.posts.update(author=deleted_profile)
        return super().delete(*args, **kwargs)

    @staticmethod
    def get_deleted_user():
        from .profiles import Profile

        deleted_user, created = User.objects.get_or_create(email=settings.DELETED_USER_EMAIL)
        if created:
            deleted_user.set_unusable_password()
            deleted_user.save(update_fields=['password'])
        deleted_profile, _ = Profile.objects.get_or_create(
            user=deleted_user,
            defaults={'first_name': 'Deleted User'}
        )
        return deleted_profile
