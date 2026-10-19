from django.core.management.base import BaseCommand
from apps.accounts.management.commands.createuser import Command as UserCreateCommand
from apps.blog.management.commands.createpost import Command as PostCreateCommand
from apps.blog.management.commands.postlike import Command as PostLikeCreateCommand
from apps.blog.management.commands.postview import Command as PostViewCreateCommand
from apps.blog.models import Post
import math
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
        result = ' RESULT '
        user_creator = UserCreateCommand()
        post_creator = PostCreateCommand()
        post_like_creator = PostLikeCreateCommand()
        post_view_creator = PostViewCreateCommand()
        post_count = 0
        post_like_count = 0
        post_view_count = 0

        dependencies = post_creator.check_dependencies()
        if not dependencies:
            msg = 'NO POST OBJECT CREATED.'
            self.stdout.write(
                '=' * (
                    math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
                ) + result + '=' * (
                    math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                )
            )
            self.stdout.write(msg)
            self.stdout.write('=' * len(msg))
            return

        for iteration in range(options.get('iteration')):
            if iteration != 0:
                self.stdout.write('\n')
            self.stdout.write(self.style.SUCCESS('=' * (len(str(iteration + 1)) + 10 + (6 * 2))))
            self.stdout.write(self.style.SUCCESS((' ' * 6) + f'ITERATION {iteration + 1}'))
            self.stdout.write(self.style.SUCCESS('=' * (len(str(iteration + 1)) + 10 + (6 * 2))))
            self.stdout.write('\n')

            stg1 = 'STAGE 1: GENERATE USER OBJECT'
            self.stdout.write('=' * (len(stg1) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg1)
            self.stdout.write('=' * (len(stg1) + (6 * 2)))
            self.stdout.write('\n')
            _, profile_obj = user_creator.handle_user_create(options.get('timeout'))

            stg2 = 'STAGE 2: GENERATE POST OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg2) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg2)
            self.stdout.write('=' * (len(stg2) + (6 * 2)))
            self.stdout.write('\n')
            posts_in_iteration = post_creator.handle_post_create(
                options.get('count') or random.randint(1, 3),
                timeout=options.get('timeout'),
                profile_obj=profile_obj
            )

            posts = Post.objects.all()

            stg3 = 'STAGE 3: GENERATE POSTLIKE OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg3) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg3)
            self.stdout.write('=' * (len(stg3) + (6 * 2)))
            self.stdout.write('\n')
            post_likes_in_iteration = post_like_creator.handle_postlike_create(
                posts=posts,
                profile_obj=profile_obj
            )

            stg4 = 'STAGE 4: GENERATE POSTVIEW OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg4) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg4)
            self.stdout.write('=' * (len(stg4) + (6 * 2)))
            self.stdout.write('\n')
            post_views_in_iteration = post_view_creator.handle_postview_create(
                posts=posts,
                profile_obj=profile_obj
            )

            post_count += posts_in_iteration
            post_like_count += post_likes_in_iteration
            post_view_count += post_views_in_iteration

        longest = lambda a, b, c: max(a, b, c, key=len)
        biggest = lambda a, b, c: max(a, b, c)

        post_msg = ' POST OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        post_like_msg = ' POSTLIKE OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        post_view_msg = ' POSTVIEW OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'

        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS(
            '=' * (
                len(str(
                    biggest(post_count, post_like_count, post_view_count)
                )) + math.ceil(len(
                    longest(post_msg, post_like_msg, post_view_msg)
                ) / 2) - math.ceil(len(result) / 2) - 1
            ) + result + '=' * (
                math.ceil(len(
                    longest(post_msg, post_like_msg, post_view_msg)
                ) / 2) - math.ceil(len(result) / 2)
            )
        ))

        if post_count != 0:
            self.stdout.write(self.style.SUCCESS(post_count + post_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO POST OBJECT CREATED.'))
        if post_like_count != 0:
            self.stdout.write(self.style.SUCCESS(post_like_count + post_like_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO POSTLIKE OBJECT CREATED.'))
        if post_view_count != 0:
            self.stdout.write(self.style.SUCCESS(post_view_count + post_view_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO POSTVIEW OBJECT CREATED.'))

        self.stdout.write(self.style.SUCCESS(
            '=' * (
                len(str(post_count)) + len(longest(post_msg, post_like_msg, post_view_msg))
            )
        ))
