from django.core.management.base import BaseCommand
from apps.accounts.management.commands.createuser import Command as UserCreateCommand
from apps.blog.models import Post
from faker import Faker
import math
import random

from ...models import Comment


class Command(BaseCommand):
    """
    A command to generate Comment objects.
    """
    help = 'Generates Comment objects'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-t', '--timeout', type=int, default=3)

    def check_dependencies(self):
        ids = list(Post.objects.values_list('pk', flat=True))
        posts_ids = random.sample(ids, k=min(20, len(ids)))
        posts = [Post.objects.get(pk=id) for id in posts_ids]

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

    def handle_comment_create(self, posts, profile_obj):
        comments = []

        for post in posts:

            if post.author == profile_obj:
                if random.choice((True, False)):
                    self.stdout.write(
                    f'Creating Comment object for post with id {post.pk}...',
                    ending=''
                )
                    comment = Comment.objects.create(
                        post=post,
                        user=profile_obj,
                        content=self.fake.text()
                    )
                    self.stdout.write(self.style.SUCCESS(' DONE'))
                    comments += [comment]

                    continue

            self.stdout.write(
                f'Creating Comment object for post with id {post.pk}...',
                ending=''
            )
            comment = Comment.objects.create(
                post=post,
                user=profile_obj,
                content=self.fake.text()
            )
            self.stdout.write(self.style.SUCCESS(' DONE'))
            comments += [comment]

        return comments

    def handle(self, *args, **options):
        result = ' RESULT '
        posts = self.check_dependencies()
        if not posts:
            msg = 'NO COMMENT OBJECT CREATED.'
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

        stg2 = 'STAGE 2: GENERATE COMMENT OBJECTS'
        self.stdout.write('\n')
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write((' ' * 6) + stg2)
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write('\n')
        comments = self.handle_comment_create(
            posts=posts,
            profile_obj=profile_obj
        )

        self.stdout.write('\n')
        match comments:
            case []:
                msg = 'NO COMMENT OBJECT CREATED.'
                self.stdout.write(
                    '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                    ) + result + '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                    )
                )
                self.stdout.write(msg)
                self.stdout.write('=' * len(msg))
            case _:
                msg = ' COMMENT OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'

                self.stdout.write(
                    '=' * (
                        len(str(len(comments))) + math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
                    ) + result + '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                    )
                )
                self.stdout.write(str(len(comments)) + msg)
                self.stdout.write(
                    '=' * (
                        len(str(len(comments))) + len(msg)
                    )
                )
