from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(default='avatars/default.jpg')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Follow(models.Model):
    following = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='followers'
    )
    follower = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='followings'
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'follower'], name='unique_user_follow'
            )
        ]

    def __str__(self):
        return self.following.email
