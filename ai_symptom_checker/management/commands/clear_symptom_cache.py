from django.core.management.base import BaseCommand
from ai_symptom_checker.models import SymptomCache


class Command(BaseCommand):
    help = 'Clear all cached symptom check results'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear all cached results',
        )

    def handle(self, *args, **options):
        if options['all']:
            count = SymptomCache.objects.all().delete()[0]
            self.stdout.write(
                self.style.SUCCESS(f'Successfully cleared {count} cached symptom results')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Use --all flag to clear all cached results')
            )

