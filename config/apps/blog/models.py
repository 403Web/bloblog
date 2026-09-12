from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, related_name='posts',
        null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.user.email

    def get_snippet(self):
        return self.content[:20] if len(self.content) >= 20 else self.content


class PostLike(models.Model):
    user = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='likes'
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.email

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'], name='unique_user_post_like'
            )
        ]


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
