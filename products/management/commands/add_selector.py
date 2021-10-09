import json

from django.core.management import BaseCommand

from products.models import ProductTypeSelectorValue, ProductTypeSelector


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('attributes.json', 'r', encoding='utf-8') as file:
            attributes = json.load(file)
        selector = ProductTypeSelector.objects.get(title='size')
        for digi_id, value in attributes.items():
            print(digi_id, value)
            ProductTypeSelectorValue.objects.create(digikala_id=digi_id,
                                                    selector=selector,
                                                    value=value)
