from django.core.management.base import BaseCommand
from apps.blog.management.commands.createpost import Command as CreatePostCommand
import random


class Command(BaseCommand):
    """
    A command for generating multiple posts with different user objects
    (as author) using "handle_post_create" method from create_post command.
    """
    help = 'Generates multiple posts with different users using create_post command'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--iteration', type=int, default=30)
        parser.add_argument('-c', '--count', type=int, default=None)
        parser.add_argument('-t', '--timeout', type=int, default=3)

    def handle(self, *args, **options):
        creator = CreatePostCommand()
        post_count = 0

        self.stdout.write('Running python manage.py createpost...')

        for iteration in range(options.get('iteration')):
            self.stdout.write('=======================')
            self.stdout.write(f'     ITERATION {iteration + 1}')
            self.stdout.write('=======================')

            posts_in_iteration = creator.handle_post_create(
                options.get('count') or random.randint(1, 3),
                timeout=options.get('timeout')
            )
            match posts_in_iteration:
                case (False, 'NO_OBJECT'):
                    break
                case (False, 'INTEGRITY_ERROR'):
                    continue

            post_count += posts_in_iteration

        if post_count != 0:
            self.stdout.write(
                    f'{post_count} POST OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
            )
        else:
            self.stdout.write('NO POST OBJECT CREATED.')
