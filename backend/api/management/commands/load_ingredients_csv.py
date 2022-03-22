import csv

from django.core.management import BaseCommand
from django.utils import timezone

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Helps ingredients csv file into Django model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options['file_path']
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            data = list(csv.reader(csv_file, delimiter=',', ))
            for row in data[0:]:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1])
        end_time = timezone.now()
        total_time = (end_time-start_time).total_seconds()
        self.stdout.write(
            self.style.SUCCESS(
                f'Loading CSV took: {total_time} seconds.'
            )
        )
