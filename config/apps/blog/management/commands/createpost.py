from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.accounts.models import Profile
from apps.blog.models import Post, Category
from faker import Faker
from django.contrib.auth import get_user_model
import requests
import random


class Command(BaseCommand):
    """
    A command to initialize the database with fake and random data for testing,
    debugging and load testing. It will be used for build command right after
    python manage.py migrate && python manage.py createcategories.
    """
    help = 'Generates fake and random data to initialize the database for testing.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-c', '--count', type=int, default=3)
        parser.add_argument('-t', '--timeout', type=int, default=3)

    def handle_post_create(self, count, timeout):
        post_count = 0

        CATEGORIES = tuple(Category.objects.all())
        if not CATEGORIES:
            self.stdout.write(
                self.style.ERROR(
                    'Category objects have not been found.'
                    ' Try running "python manage.py createcategories" first.'
                )
            )
            return 0

        self.stdout.write('Creating new user object...', ending='')
        user_obj = get_user_model().objects.create_user(
            email=self.fake.email(), password='a/@234a/?'
        )
        self.stdout.write(self.style.SUCCESS(' SUCCESSFUL'))
        self.stdout.write(f'email: {user_obj.email}')

        self.stdout.write('Getting user profile object...', ending='')
        profile_obj = Profile.objects.get(user=user_obj)
        self.stdout.write(self.style.SUCCESS('SUCCESSFUL'))
        self.stdout.write(f'name: {profile_obj.name}')

        url = f'https://api.dicebear.com/9.x/avataaars/png?seed={profile_obj.name}'
        self.stdout.write('Setting avatar for user profile object...', ending='')
        try:
            profile_obj.avatar.save(
                f'avatar_{profile_obj.name}.png',
                ContentFile(requests.get(url, timeout=timeout).content)
            )
            self.stdout.write(self.style.SUCCESS(' SUCCESSFUL'))
        except requests.exceptions.Timeout:
            self.stdout.write(
                self.style.WARNING(' Request timed out for avatar, SKIPPING...')
            )
        except requests.exceptions.RequestException:
            self.stdout.write(
                self.style.WARNING(' Request failed for avatar, SKIPPING...')
            )

        for idx in range(count):
            width = random.randint(100, 1000)
            height = random.randint(100, 800)
            url = f'https://random.imagecdn.app/{width}/{height}'

            self.stdout.write(
                f'Creating {idx + 1} post(s) for user "{profile_obj.name}"...',
                ending=''
            )

            post = Post.objects.create(
                author=profile_obj,
                title=self.fake.text(max_nb_chars=200),
                content=self.fake.paragraph(nb_sentences=random.randint(10, 100)),
                category=random.choice(CATEGORIES)
            )
            try:
                post.image.save(
                    f'img_{profile_obj.name}_{idx + 1}.jpg',
                    ContentFile(requests.get(url, timeout=timeout).content)
                )
            except requests.exceptions.Timeout:
                self.stdout.write(
                    self.style.WARNING(' Request timed out for image, SKIPPING...'),
                    ending=''
                )
            except requests.exceptions.RequestException:
                self.stdout.write(
                    self.style.WARNING(' Request failed for image, SKIPPING...'),
                    ending=''
                )

            post_count += 1
            self.stdout.write(self.style.SUCCESS(' DONE'))

        return post_count

    def handle(self, *args, **options):
        post_count = self.handle_post_create(
            count=options.get('count'), timeout=options.get('timeout')
        )

        if post_count != 0:
            self.stdout.write(f'{post_count} POST OBJECTS HAVE BEEN CREATED SUCCESSFULLY.')
        else:
            self.stdout.write('NO POST OBJECT CREATED,')
