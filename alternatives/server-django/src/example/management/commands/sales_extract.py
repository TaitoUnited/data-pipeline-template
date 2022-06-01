from django.core.management.base import BaseCommand
from src.example.models import Sales


class Command(BaseCommand):
    help = "SalesExtraxt example command"

    # def add_arguments(self, parser):

    def handle(self, *args, **options):
        print("Example implementation that runs once.")
        sales = Sales.objects.all()
        print(sales)
