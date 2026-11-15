from django.core.management.base import BaseCommand
from psychbuddy.db_migrator import migrate_and_seed

class Command(BaseCommand):
    help = 'Migrates MySQL database tables and seeds rich sample data for the frontend'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Drop and recreate all tables before seeding'
        )

    def handle(self, *args, **options):
        reset = options.get('reset', False)
        self.stdout.write(self.style.NOTICE('Starting database migration and sample data seeding...'))
        migrate_and_seed(drop_existing=reset, clear_existing=reset)
        self.stdout.write(self.style.SUCCESS('Database migration and sample seeding completed successfully!'))
