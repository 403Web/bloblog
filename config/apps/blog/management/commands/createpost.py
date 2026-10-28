from django.core.management.base import BaseCommand
from apps.accounts.management.commands.createuser import Command as UserCreateCommand
from django.core.files.base import ContentFile
from apps.blog.models import Post, Category
from faker import Faker
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import requests
import random
import math


CATEGORIES = tuple(Category.objects.all())
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

    def check_dependencies(self):
        if not CATEGORIES:
            self.stdout.write(
                self.style.ERROR(
                    'Category objects have not been found.\n'
                    'Try running "python manage.py createcategories" or'
                    ' "python manage.py db_init" first.\n'
                )
            )
            return False
        return True

    def handle_user_create(self, timeout):
        user_creator = UserCreateCommand()
        return user_creator.handle_user_create(timeout)

    def handle_post_create(self, count, timeout, profile_obj):
        posts = []

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

            posts += [post]
            self.stdout.write(self.style.SUCCESS(' DONE'))

        return posts

    def handle(self, *args, **options):
        result = ' RESULT '
        dependencies = self.check_dependencies()
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

        stg1 = 'STAGE 1: GENERATE USER OBJECT'
        self.stdout.write('=' * (len(stg1) + (6 * 2)))
        self.stdout.write((' ' * 6) + stg1)
        self.stdout.write('=' * (len(stg1) + (6 * 2)))
        self.stdout.write('\n')
        _, profile_obj = self.handle_user_create(options.get('timeout'))

        stg2 = 'STAGE 2: GENERATE POST OBJECTS'
        self.stdout.write('\n')
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write((' ' * 6) + stg2)
        self.stdout.write('=' * (len(stg2) + (6 * 2)))
        self.stdout.write('\n')
        posts = self.handle_post_create(
            count=options.get('count'),
            timeout=options.get('timeout'),
            profile_obj=profile_obj
        )

        msg = ' POST OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        self.stdout.write('\n')
        self.stdout.write(
            '=' * (
                len(str(len(posts))) + math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
            ) + result + '=' * (
                math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
            )
        )
        self.stdout.write(str(len(posts)) + msg)
        self.stdout.write(
            '=' * (
                len(str(len(posts))) + len(msg)
            )
        )
