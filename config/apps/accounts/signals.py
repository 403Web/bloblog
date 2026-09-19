from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
import os

from .models import Profile


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_on_user_create(sender, instance, created, **kwargs):
    if created and instance.email != settings.DELETED_USER_EMAIL:
        Profile.objects.create(
            user=instance, name=instance.email.split('@')[0]
        )


@receiver(pre_delete, sender=User)
def set_post_and_comment_author_to_deleted_user_on_user_delete(
    sender, instance, **kwargs
):
    if instance.email != settings.DELETED_USER_EMAIL:
        deleted_user, created = User.objects.get_or_create(email=settings.DELETED_USER_EMAIL)

        if created:
            deleted_user.set_unusable_password()
            deleted_user.save(update_fields=['password'])

        deleted_profile, _ = Profile.objects.get_or_create(
            user=deleted_user,
            defaults={'name': 'Deleted User'}
        )

        instance.profile.posts.update(author=deleted_profile)
        instance.profile.comments.update(user=deleted_profile)


@receiver(pre_save, sender=Profile)
def delete_previous_avatar_on_profile_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        profile = sender.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return

    old_avatar = profile.avatar
    new_avatar = instance.avatar

    if (
        old_avatar and
        os.path.isfile(old_avatar.path) and
        old_avatar.name != 'avatars/default.jpg' and
        new_avatar != old_avatar
    ):
        old_avatar.delete(save=False)


@receiver(pre_delete, sender=User)
def delete_avatar_on_user_delete(sender, instance, **kwargs):
    avatar = Profile.objects.get(user=instance).avatar

    if (
        avatar and
        os.path.isfile(avatar.path) and
        avatar.name != 'avatars/default.jpg'
    ):
        avatar.delete(save=False)
