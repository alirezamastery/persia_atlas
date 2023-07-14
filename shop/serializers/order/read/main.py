from rest_framework import serializers

from shop.models import *
from .sub import *


__all__ = [
    'OrderReadSerializer',
]


class OrderReadSerializer(serializers.ModelSerializer):
    items = _OrderItemReadSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price_sum', 'items', 'is_canceled']
