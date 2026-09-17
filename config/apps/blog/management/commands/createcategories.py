from django.core.management.base import BaseCommand

from ...models import Category


CATEGORIES = [
    'Technology',
    'Programming',
    'Science',
    'Mathematics',
    'Artificial Intelligence',
    'Cybersecurity',
    'Gadgets',
    'Internet',
    'Education',
    'Books',
    'Movies & TV',
    'Music',
    'Gaming',
    'Cars',
    'Travel',
    'Lifestyle',
    'Business',
    'Finance',
    'Psychology',
    'Philosophy',
    'History',
    'News',
    'Reviews',
    'Tutorials',
    'Personal',
    'Other'
]


class Command(BaseCommand):
    """
    A command to initialize the database with the specified categories
    in the list above. It will be used for build command right after
    python manage.py migate.
    """
    help = 'Creates category objects and initializes the database.'

    def handle(self, *args, **options):
        cat_count = 0

        for cat in CATEGORIES:
            if Category.objects.filter(name=cat).exists():
                self.stdout.write(
                    f'Category object "{self.style.SUCCESS(cat)}" already exists...'
                    f'{self.style.WARNING(" SKIPPING")}'
                )
                continue

            self.stdout.write(
                f'Creating category object "{self.style.WARNING(cat)}"...',
                ending=''
            )

            Category.objects.create(name=cat)
            self.stdout.write(self.style.SUCCESS(' DONE'))
            cat_count += 1

        if cat_count == 0:
            self.stdout.write('NO CATEGORY OBJECT CREATED.')
        else:
            self.stdout.write(
                f'{cat_count} CATEGORY OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
            )
        
