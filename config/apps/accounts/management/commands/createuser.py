from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.accounts.models import Profile
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from faker import Faker
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import requests
import random


class Command(BaseCommand):
    """
    A command to create users that will be used by other commands.
    """
    help = 'Creates User object'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-t', '--timeout', type=int, default=3)

    def handle_user_create(self, timeout):
        self.stdout.write('Creating new user object...', ending='')
        try:
            user_obj = get_user_model().objects.create_user(
                email=self.fake.email(),
                username=self.fake.user_name(),
                password='a/@234a/?'
            )
        except IntegrityError:
            self.stdout.write(self.style.WARNING(
                ' Unique constraint failed: accounts.User.email, SKIPPING'
            ))
            return (False, 'INTEGRITY_ERROR')
        self.stdout.write(self.style.SUCCESS(' SUCCESSFUL'))
        self.stdout.write(f'email: {user_obj.email}, id: {user_obj.pk}')

        self.stdout.write('Getting user profile object...', ending='')
        profile_obj = Profile.objects.get(user=user_obj)
        self.stdout.write(self.style.SUCCESS(' SUCCESSFUL'))
        self.stdout.write(f'name: {profile_obj.name}, id: {profile_obj.pk}')

        size = random.randint(150, 600)
        url = f'https://i.pravatar.cc/{size}?img={profile_obj.name}'
        self.stdout.write('Setting avatar for user profile object...', ending='')
        try:
            response = requests.get(url, timeout=timeout)

            if (
                response.status_code == 200 and
                response.headers.get('Content-Type', '').startswith('image/')
            ):
                try:
                    img_format = Image.open(BytesIO(response.content)).format.lower()
                    profile_obj.avatar.save(
                        f'avatar_{profile_obj.name}.{img_format}',
                        ContentFile(response.content)
                    )

                    self.stdout.write(self.style.SUCCESS(' SUCCESSFUL'))
                    self.stdout.write(f'location: {profile_obj.avatar.name}')

                except UnidentifiedImageError:
                    self.stdout.write(
                        self.style.WARNING(' Invalid avatar response, SKIPPING')
                    )

            else:
                self.stdout.write(
                    self.style.WARNING(' Invalid avatar response, SKIPPING')
                )

        except requests.exceptions.Timeout:
            self.stdout.write(
                self.style.WARNING(' Request timed out for avatar, SKIPPING')
            )
        except requests.exceptions.RequestException:
            self.stdout.write(
                self.style.WARNING(' Request failed for avatar, SKIPPING')
            )

        return (user_obj, profile_obj)

    def handle(self, *args, **options):
        self.handle_user_create(options.get('timeout'))
