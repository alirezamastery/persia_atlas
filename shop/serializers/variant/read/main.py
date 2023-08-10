from rest_framework import serializers

from shop.models import *
from .sub import *


__all__ = [
    'VariantReadSerializer',
]


class VariantReadSerializer(serializers.ModelSerializer):
    product = _ProductSerializer(read_only=True)
    selector_value = _VariantSelectorValueReadSerializer(read_only=True)

    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'selector_value',
            'is_active',
            'price',
            'inventory',
            'max_in_order',
        ]
