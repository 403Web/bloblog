from django.db import models
from apps.accounts.models import Profile


class Post(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='author'
    )
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.user.email
