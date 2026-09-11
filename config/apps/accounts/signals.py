from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Profile


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created and instance.email != settings.DELETED_USER_EMAIL:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=User)
def set_user_posts_author_to_deleted_user(sender, instance, **kwargs):
    if instance.email != settings.DELETED_USER_EMAIL:
        deleted_user, created = User.objects.get_or_create(email=settings.DELETED_USER_EMAIL)
        if created:
            deleted_user.set_unusable_password()
            deleted_user.save(update_fields=['password'])
        deleted_profile, _ = Profile.objects.get_or_create(
            user=deleted_user,
            defaults={'first_name': 'Deleted User'}
        )
        instance.profile.posts.update(author=deleted_profile)
        instance.profile.comments.update(user=deleted_profile)
