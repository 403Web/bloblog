from django.core.management.base import BaseCommand
from apps.accounts.management.commands.createuser import Command as UserCreateCommand
from django.db import IntegrityError
import math
import random

from ...models import Post, PostLike


class Command(BaseCommand):
    """
    A command to create PostLike objects.
    """
    help = 'Creates PostLike objects'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--timeout', type=int, default=3)

    def check_dependencies(self):
        posts = Post.objects.all()
        if not posts:
            self.stdout.write(
                self.style.ERROR(
                    'No Post object found.\n'
                    'Try running "python manage.py createpost" first.\n'
                )
            )
            return False
        return posts

    def handle_user_create(self, timeout):
        user_creator = UserCreateCommand()
        return user_creator.handle_user_create(timeout)

    def handle_postlike_create(self, posts, profile_obj):
        post_like_count = 0

        for post in posts:

            if post.author == profile_obj:
                if random.choice((True, False, False, False)):
                    self.stdout.write(
                    f'Creating PostLike object for post with id {post.pk}...',
                    ending=''
                )
                    try:
                        PostLike.objects.create(
                            post=post, user=profile_obj
                        )
                        self.stdout.write(self.style.SUCCESS(' DONE'))
                        post_like_count += 1
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(
                            'Unique constraint failed, SKIPPING'
                        ))

                    continue

            if random.choice((True, False)):
                self.stdout.write(
                    f'Creating PostLike object for post with id {post.pk}...',
                    ending=''
                )
                try:
                    PostLike.objects.create(
                        post=post, user=profile_obj
                    )
                    self.stdout.write(self.style.SUCCESS(' DONE'))
                    post_like_count += 1
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(
                        'Unique constraint failed, SKIPPING'
                    ))

        return post_like_count

    def handle(self, *args, **options):
        result = ' RESULT '
        posts = self.check_dependencies()
        if not posts:
            msg = 'NO POSTLIKE OBJECT CREATED.'
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

        stg1 = 'STAGE 1: GENERATE USER OBJECT'
        self.stdout.write('=' * (len(stg1) + (6 * 2)))
        self.stdout.write((' ' * 6) + stg1)
        self.stdout.write('=' * (len(stg1) + (6 * 2)))
        self.stdout.write('\n')
        _, profile_obj = self.handle_user_create(options.get('timeout'))

        stg2 = 'STAGE 2: GENERATE POSTLIKE OBJECTS'
        self.stdout.write('\n')
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write((' ' * 6) + stg2)
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write('\n')
        post_like_count = self.handle_postlike_create(
            posts=posts,
            profile_obj=profile_obj
        )

        self.stdout.write('\n')
        match post_like_count:
            case 0:
                msg = 'NO POSTLIKE OBJECT CREATED.'
                self.stdout.write(
                    '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
                    ) + result + '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                    )
                )
                self.stdout.write(msg)
                self.stdout.write('=' * len(msg))
            case _:
                msg = ' POSTLIKE OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'

                self.stdout.write(
                    '=' * (
                        len(str(post_like_count)) + math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
                    ) + result + '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                    )
                )
                self.stdout.write(str(post_like_count) + msg)
                self.stdout.write(
                    '=' * (
                        len(str(post_like_count)) + len(msg)
                    )
                )
