from rest_framework import serializers

from shop.models import *


__all__ = [
    '_OrderItemReadSerializer',
]


class _OrderItemVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product_id', 'selector_value_id', 'is_active']


class _OrderItemReadSerializer(serializers.ModelSerializer):
    item = _OrderItemVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'price', 'quantity']
