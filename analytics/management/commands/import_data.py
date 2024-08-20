import csv
from django.core.management.base import BaseCommand
from analytics.models import Data


class Command(BaseCommand):
    help = "Import data from CSV file into the Data model"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="The path to the CSV file.")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Data.objects.create(
                    customer_id=row["customer_id"],
                    revenue=float(row["revenue"]),
                    conversions=int(row["conversions"]),
                    status=row["status"],
                    type=row["type"],
                    category=row["category"],
                )
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
