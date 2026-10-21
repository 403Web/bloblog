from django.core.management.base import BaseCommand
from apps.accounts.management.commands.createuser import Command as UserCreateCommand
from django.db import IntegrityError
import math
import random

from ...models import Comment, CommentLike


class Command(BaseCommand):
    """
    A command to create CommentLike objects.
    """
    help = 'Creates CommentLike objects'

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

    def handle_commentlike_create(self, comments, profile_obj):
        comment_like_count = 0

        for comment in comments:

            if comment.user == profile_obj:
                if random.choice((True, False, False, False, False, False)):
                    self.stdout.write(
                    f'Creating CommentLike object for comment with id {comment.pk}...',
                    ending=''
                )
                    try:
                        CommentLike.objects.create(
                            comment=comment, user=profile_obj
                        )
                        self.stdout.write(self.style.SUCCESS(' DONE'))
                        comment_like_count += 1
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(
                            'Unique constraint failed, SKIPPING'
                        ))

                    continue

            if random.choice((True, False)):
                self.stdout.write(
                    f'Creating CommentLike object for comment with id {comment.pk}...',
                    ending=''
                )
                try:
                    CommentLike.objects.create(
                        comment=comment, user=profile_obj
                    )
                    self.stdout.write(self.style.SUCCESS(' DONE'))
                    comment_like_count += 1
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(
                        'Unique constraint failed, SKIPPING'
                    ))

        return comment_like_count

    def handle(self, *args, **options):
        result = ' RESULT '
        comments = self.check_dependencies()
        if not comments:
            msg = 'NO COMMENTLIKE OBJECT CREATED.'
            self.stdout.write(
                '=' * (
                    math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
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

        stg2 = 'STAGE 2: GENERATE COMMENTLIKE OBJECTS'
        self.stdout.write('\n')
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write((' ' * 6) + stg2)
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write('\n')
        comment_like_count = self.handle_commentlike_create(
            comments=comments,
            profile_obj=profile_obj
        )

        self.stdout.write('\n')
        match comment_like_count:
            case 0:
                msg = 'NO COMMENTLIKE OBJECT CREATED.'
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
                msg = ' COMMENTLIKE OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'

                self.stdout.write(
                    '=' * (
                        len(str(comment_like_count)) + math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
                    ) + result + '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                    )
                )
                self.stdout.write(str(comment_like_count) + msg)
                self.stdout.write(
                    '=' * (
                        len(str(comment_like_count)) + len(msg)
                    )
                )
