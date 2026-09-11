from django.db import models
from apps.accounts.models import Profile
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.user.email


class PostLike(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes'
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.email

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post_like'
            )
        ]
