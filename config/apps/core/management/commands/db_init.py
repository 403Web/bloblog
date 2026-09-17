from django.core.management.base import BaseCommand
from django.core.management import call_command, CommandError


class Command(BaseCommand):
    """
    A command to initialize the database with basic needed data and get it
    ready to use. It will be used right after python manage.py migrate and
    contains other commands (no more commands are required).
    """
    help = 'Initialized the database for use.'

    def handle(self, *args, **options):
        try:
            call_command('createcategories')
            call_command('create_deleted_user')
        except Exception as error:
            raise CommandError(f'INITIALIZATION FAILED: {error}')
