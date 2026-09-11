from django.db import models
from apps.accounts.models import Profile
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


def get_deleted_user():
    deleted_user, created = User.objects.get_or_create(email=settings.DELETED_USER_EMAIL)
    if created:
        deleted_user.set_unusable_password()
        deleted_user.save(update_fields=['password'])
    deleted_profile, _ = Profile.objects.get_or_create(
        user=deleted_user,
        defaults={'first_name': 'Deleted User'}
    )
    return deleted_profile


class Post(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.SET(get_deleted_user), related_name='posts'
    )
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.user.email
