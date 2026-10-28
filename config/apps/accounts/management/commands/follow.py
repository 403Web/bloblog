from django.core.management.base import BaseCommand
from apps.accounts.management.commands.createuser import Command as UserCreateCommand
from django.db import IntegrityError
import math
import random

from ...models import Profile, Follow


class Command(BaseCommand):
    """
    A command to create Follow objects.
    """
    help = 'Creates Follow objects'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--timeout', type=int, default=3)

    def check_dependencies(self):
        ids = list(Profile.objects.values_list('pk', flat=True))
        profiles_ids = random.sample(ids, k=min(10, len(ids)))
        profiles = [Profile.objects.get(pk=id) for id in profiles_ids]

        if not profiles:
            self.stdout.write(
                self.style.ERROR(
                    'No User object found.\n'
                    'Try running "python manage.py createuser" first.\n'
                )
            )
            return False
        return profiles

    def handle_user_create(self, timeout):
        user_creator = UserCreateCommand()
        return user_creator.handle_user_create(timeout)

    def handle_follow_create(self, profiles, profile_obj):
        follows_count = 0

        for profile in profiles:

            self.stdout.write(
                f'Creating Follow object for User (Profile) with id {profile.pk}...',
                ending=''
            )
            try:
                Follow.objects.create(
                    following=profile, follower=profile_obj
                )
                self.stdout.write(self.style.SUCCESS(' DONE'))
                follows_count += 1
            except IntegrityError:
                self.stdout.write(self.style.WARNING(
                    'Unique constraint failed, SKIPPING'
                ))

        return follows_count

    def handle(self, *args, **options):
        result = ' RESULT '
        profiles = self.check_dependencies()
        if not profiles:
            msg = 'NO FOLLOW OBJECT CREATED.'
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

        stg2 = 'STAGE 2: GENERATE FOLLOW OBJECTS'
        self.stdout.write('\n')
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write((' ' * 6) + stg2)
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write('\n')
        follows_count = self.handle_follow_create(
            profiles=profiles,
            profile_obj=profile_obj
        )

        self.stdout.write('\n')
        match follows_count:
            case 0:
                msg = 'NO FOLLOW OBJECT CREATED.'
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
                msg = ' FOLLOW OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'

                self.stdout.write(
                    '=' * (
                        len(str(follows_count)) + math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
                    ) + result + '=' * (
                        math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                    )
                )
                self.stdout.write(str(follows_count) + msg)
                self.stdout.write(
                    '=' * (
                        len(str(follows_count)) + len(msg)
                    )
                )
