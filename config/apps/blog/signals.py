from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
import os

from .models import Post


@receiver(pre_save, sender=Post)
def delete_previous_img_on_post_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        post = Post.objects.get(pk=instance.pk)
    except Post.DoesNotExist:
        return

    old_img = post.image
    new_img = instance.image

    if (
        old_img and
        os.path.isfile(old_img.path) and
        old_img.name != 'posts/default.jpg' and
        new_img != old_img
    ):
        old_img.delete(save=False)


@receiver(pre_delete, sender=Post)
def delete_img_on_post_delete(sender, instance, **kwargs):
    img = instance.image

    if (
        img and
        os.path.isfile(img.path) and
        img.name != 'posts/default.jpg'
    ):
        img.delete(save=False)
