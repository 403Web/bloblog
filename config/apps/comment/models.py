from django.db import models
from apps.accounts.models import Profile
from apps.blog.models import Post


class Comment(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='replies',
        blank=True, null=True
    )
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user.email
