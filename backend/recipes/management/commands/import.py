"""
Для импорта ингредиентов выполнить команду:
python manage.py import
--path "/home/sergey/Dev/foodgram-project-react/data/ingredients.json"
"""

import json

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Import ingredients from json file"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="file path")

    def handle(self, *args, **options):
        file_path = options["path"]

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                try:
                    Ingredient.objects.create(
                        name=item["name"], measurement_unit=item["measurement_unit"]
                    )
                except IntegrityError as err:
                    line = ", ".join(data)
                    self.stdout.write(f'Error! {err}, "{line}"')
