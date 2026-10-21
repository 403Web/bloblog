from django.core.management.base import BaseCommand
from apps.accounts.management.commands.createuser import Command as UserCreateCommand
from faker import Faker
import math
import random

from ...models import Comment


class Command(BaseCommand):
    """
    A command to generate Comment reply objects.
    """
    help = 'Generates Comment reply objects'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-t', '--timeout', type=int, default=3)

    def check_dependencies(self):
        comments = Comment.objects.all()
        if not comments:
            self.stdout.write(
                self.style.ERROR(
                    'No Comment object found.\n'
                    'Try running "python manage.py comment" first.\n'
                )
            )
            return False
        return comments

    def handle_user_create(self, timeout):
        user_creator = UserCreateCommand()
        return user_creator.handle_user_create(timeout)

    def handle_reply_create(self, comments, profile_obj):
        reply_count = 0

        for comment in comments:

            if comment.user == profile_obj:
                if random.choice((True, False, False, False, False, False)):
                    self.stdout.write(
                    f'Creating Comment (reply) object for comment with id {comment.pk}...',
                    ending=''
                )
                    Comment.objects.create(
                        post=comment.post,
                        parent=comment,
                        user=profile_obj,
                        content=self.fake.text()
                    )
                    self.stdout.write(self.style.SUCCESS(' DONE'))
                    reply_count += 1

                    continue

            if random.choice((True, False)):
                self.stdout.write(
                    f'Creating Comment (reply) object for comment with id {comment.pk}...',
                    ending=''
                )
                Comment.objects.create(
                    post=comment.post,
                    parent=comment,
                    user=profile_obj,
                    content=self.fake.text()
                )
                self.stdout.write(self.style.SUCCESS(' DONE'))
                reply_count += 1

        return reply_count

    def handle(self, *args, **options):
        result = ' RESULT '
        comments = self.check_dependencies()
        if not comments:
            msg = 'NO COMMENT (REPLY) OBJECT CREATED.'
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

        stg2 = 'STAGE 2: GENERATE COMMENT (REPLY) OBJECTS'
        self.stdout.write('\n')
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write((' ' * 6) + stg2)
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write('\n')
        reply_count = self.handle_reply_create(
            comments=comments,
            profile_obj=profile_obj
        )

        self.stdout.write('\n')
        match reply_count:
            case 0:
                msg = 'NO COMMENT (REPLY) OBJECT CREATED.'
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
                msg = ' COMMENT (REPLY) OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'

                self.stdout.write(
                    '=' * (
                        len(str(reply_count)) + math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
                    ) + result + '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                    )
                )
                self.stdout.write(str(reply_count) + msg)
                self.stdout.write(
                    '=' * (
                        len(str(reply_count)) + len(msg)
                    )
                )
