from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.accounts.models import Profile
from apps.blog.models import Post, Category
from faker import Faker
from django.contrib.auth import get_user_model
import requests
import random


COLORS = ('white', 'blue', 'red', 'yellow', 'cyan', 'brown')
FORMATS = ('png', 'jpg', 'jpeg')


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

    def handle_post_create(self, count):
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

        user_obj = get_user_model().objects.create_user(
            email=self.fake.email(), password='a/@234a/?'
        )
        profile_obj = Profile.objects.get(user=user_obj)

        for idx in range(count):
            width = random.randint(100, 1000)
            height = random.randint(100, 800)
            color = random.choice(COLORS)
            img_format = random.choice(FORMATS)
            url = f'https://placehold.co/{width}x{height}/{color}/black.{img_format}'

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
                    f'img_{profile_obj.name}_{idx + 1}.{img_format}',
                    ContentFile(requests.get(url, timeout=3).content)
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
        post_count = self.handle_post_create(count=options.get('count'))

        if post_count != 0:
            self.stdout.write(f'{post_count} POST OBJECTS HAVE BEEN CREATED SUCCESSFULLY.')
        else:
            self.stdout.write('NO POST OBJECT CREATED,')
