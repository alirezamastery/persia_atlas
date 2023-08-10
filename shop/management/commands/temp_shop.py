from django.core.management import BaseCommand
from django.db.models import *
from django.db.models.functions import *

from shop.models import *
from shop.serializers import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        total_inv_subq = Variant.objects \
            .values('product_id') \
            .filter(product=OuterRef('id')) \
            .annotate(sum=Sum('inventory')) \
            .values('sum')
        min_price_subq = Variant.objects \
            .values('product_id') \
            .filter(product=OuterRef('id')) \
            .annotate(min=Min('price')) \
            .values('min')

        qs = Product.objects \
            .select_related('brand') \
            .select_related('category') \
            .prefetch_related('variants__selector_value__type') \
            .all() \
            .annotate(total_inv=Coalesce(Subquery(total_inv_subq), Value(0))) \
            .annotate(min_price=Subquery(min_price_subq)) \
            .order_by('-total_inv')

        print(qs)
        for product in qs:
            print('total_inv:', product.total_inv)
            print('min_price:', product.min_price)
