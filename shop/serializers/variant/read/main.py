from rest_framework import serializers

from shop.models import *
from .sub import *


__all__ = [
    'ProductVariantReadSerializer',
]


class ProductVariantReadSerializer(serializers.ModelSerializer):
    product = _ProductSerializer(read_only=True)
    selector_value = _VariantSelectorValueReadSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'product',
            'selector_value',
            'is_active',
            'price',
            'inventory',
            'max_in_order',
        ]
