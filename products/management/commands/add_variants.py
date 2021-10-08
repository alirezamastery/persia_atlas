import json

from django.core.management import BaseCommand

from products.models import Product, ProductVariant, ProductTypeSelectorValue


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('variants.json', 'r', encoding='utf-8') as file:
            variants = json.load(file)
        for variant in variants:
            print(variant)
            product_obj = Product.objects.get(pk=variant['product_id'])
            selector_obj = ProductTypeSelectorValue.objects.get(digikala_id=str(variant['selector_values']))
            variant_obj = ProductVariant.objects.create(dkpc=variant['dkpc'],
                                                        product=product_obj,
                                                        price_min=variant['price_min'])
            variant_obj.selector_values.add(selector_obj)
            variant_obj.save()
