from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.accounts.models import Profile
from apps.blog.models import Post, Category
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from faker import Faker
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import requests
import random


RATIOS = [
    (16, 9),
    (4, 3),
    (3, 2)
]


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
                    ' Try running "python manage.py createcategories" or'
                    ' "python manage.py db_init" first.'
                )
            )
            return (False, 'NO_OBJECT')

        self.stdout.write('Creating new user object...', ending='')
        try:
            user_obj = get_user_model().objects.create_user(
                email=self.fake.email(), password='a/@234a/?'
            )
        except IntegrityError:
            self.stdout.write(self.style.WARNING(
                ' Unique constraint failed: accounts.User.email, SKIPPING'
            ))
            return (False, 'INTEGRITY_ERROR')
        self.stdout.write(self.style.SUCCESS(' SUCCESSFUL'))
        self.stdout.write(f'email: {user_obj.email}')

        self.stdout.write('Getting user profile object...', ending='')
        profile_obj = Profile.objects.get(user=user_obj)
        self.stdout.write(self.style.SUCCESS(' SUCCESSFUL'))
        self.stdout.write(f'name: {profile_obj.name}')

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

        for idx in range(count):
            ratio = random.choice(RATIOS)
            width = random.randint(600, 1200)
            height = int(width * (ratio[1] / ratio[0]))
            url = f'https://loremflickr.com/{width}/{height}'

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
                response = requests.get(url, timeout=timeout)

                if (
                    response.status_code == 200 and
                    response.headers.get('Content-Type', '').startswith('image/')
                ):
                    try:
                        img_format = Image.open(BytesIO(response.content)).format.lower()
                        post.image.save(
                            f'img_{profile_obj.name}_{idx + 1}.{img_format}',
                            ContentFile(response.content)
                        )
                    except UnidentifiedImageError:
                        self.stdout.write(
                            self.style.WARNING(' Invalid image response, SKIPPING...'),
                            ending=''
                        )
    
                else:
                    self.stdout.write(
                        self.style.WARNING(' Invalid image response, SKIPPING...'),
                        ending=''
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

        match post_count:
            case (False, 'NO_OBJECT'):
                self.stdout.write('NO POST OBJECT CREATED.')
            case (False, 'INTEGRITY_ERROR'):
                pass
            case _:
                self.stdout.write(f'{post_count} POST OBJECTS HAVE BEEN CREATED SUCCESSFULLY.')
