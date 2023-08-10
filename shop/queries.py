from django.db.models import Prefetch

from shop.models import *


__all__ = [
    'get_product_with_attrs',
]


def get_product_with_attrs(product_id: int):
    prefetch_attrs = Prefetch(
        'attribute_values',
        queryset=ProductAttributeValue.objects
            .filter(product_id=product_id)
            .select_related('attribute')
    )
    return Product.objects \
        .select_related('brand') \
        .select_related('category__selector_type') \
        .prefetch_related(prefetch_attrs) \
        .get(id=product_id)
