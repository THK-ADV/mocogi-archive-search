from django.core.management.base import BaseCommand
from modules.initialData import InitialData


class Command(BaseCommand):
    help = 'Load main data from an external server before starting the server'

    def handle(self, *args, **options):
        print(self.help)
        initial_data: InitialData = InitialData()
        initial_data.parse_modules()
        initial_data.parse_commits()
        initial_data.scan_commits()
