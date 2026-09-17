from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

from ...models import Profile


class Command(BaseCommand):
    """
    A command to created a deleted user object that will be used to be replaced
    with deleted users' posts' "user" field.
    """
    help = 'Creates the deleted user.'

    def handle(self, *args, **options):
        User = get_user_model()

        deleted_user, created = User.objects.get_or_create(
            email=settings.DELETED_USER_EMAIL
        )
        if created:
            deleted_user.set_unusable_password()
            deleted_user.save(update_fields=['password'])
        Profile.objects.get_or_create(
            user=deleted_user, defaults={'name': 'Deleted User'}
        )

        if created:
            self.stdout.write(self.style.SUCCESS('DELETED USER OBJECT HAS BEEN CREATED SUCCESSFULLY.'))
        else:
            self.stdout.write(self.style.WARNING('DELETED USER OBJECT ALREADY EXISTS.'))
