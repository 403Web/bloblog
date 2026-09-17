from django.core.management.base import BaseCommand
from apps.core.management.commands.create_post import Command as CreatePostCommand


class Command(BaseCommand):
    """
    A command for generating multiple posts with different user objects
    (as author) using "handle_post_create" method from create_post command.
    """
    help = 'Generates multiple posts with different users using create_post command'

    def handle(self, *args, **options):
        creator = CreatePostCommand()
        post_count = 0

        self.stdout.write('Running python manage.py create_post...')

        for _ in range(7):
            post_count += creator.handle_post_create()

        if post_count != 0:
            self.stdout.write(
                    f'{post_count} POST OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
            )
        else:
            self.stdout.write('NO POST OBJECT CREATED.')
