from django.db.models import Prefetch
from rest_framework import serializers

from shop.models import *


__all__ = [
    'OrderReadSerializer',
    'OrderWriteSerializer',
]


class OrderItemVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product_id', 'selector_value_id', 'is_active']


class OrderItemReadSerializer(serializers.ModelSerializer):
    item = OrderItemVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'price', 'quantity']


class OrderItemWriteSerializer(serializers.Serializer):
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    quantity = serializers.IntegerField()

    class Meta:
        fields = ['variant', 'quantity']


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price_sum', 'items', 'is_canceled']


class OrderWriteSerializer(serializers.ModelSerializer):
    items = serializers.ListSerializer(child=OrderItemWriteSerializer(), allow_empty=False)

    class Meta:
        model = Order
        fields = ['user', 'items']

    def create(self, validated_data):
        user = validated_data['user']
        items = validated_data['items']

        price_sum = sum(item['quantity'] * item['variant'].price for item in items)
        order = Order.objects.create(user=user, price_sum=price_sum)

        for item in items:
            OrderItem.objects.create(
                order=order,
                item=item['variant'],
                price=item['variant'].price,
                quantity=item['quantity']
            )

        order = Order.objects \
            .select_related('user') \
            .prefetch_related(Prefetch('items', queryset=OrderItem.objects.all())) \
            .get(id=order.id)

        return order

    def to_representation(self, instance: Order) -> dict:
        return OrderReadSerializer(instance).data
