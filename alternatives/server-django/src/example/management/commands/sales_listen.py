import time
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "SalesListen example command"

    def add_arguments(self, parser):
        print("No args")

    def handle(self, *args, **options):
        while True:
            print("Example implementation that just keeps on running.")
            time.sleep(60)
