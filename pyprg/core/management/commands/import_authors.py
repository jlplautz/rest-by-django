import argparse
import csv
from django.core.management.base import BaseCommand

from pyprg.core.models import Author


class Command(BaseCommand):
    help = 'importa os autores a partit de csv'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        with options['csv'] as f:
            reader = csv.reader(f)
            next(reader)

            batch = []
            count = 0

            for row in reader:
                batch.append(Author(name=row[0]))
                count += 1

                if len(batch) == 10_000:
                    Author.objects.bulk_create(batch)
                    batch.clear()
                    self.stdout.write(f'{count} Dados Inportados')

            if batch:
                Author.objects.bulk_create(batch)
                self.stdout.write(f'{count} Dados Inportados')
