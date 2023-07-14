from rest_framework import serializers

from shop.models import *


__all__ = [
    '_OrderItemWriteSerializer',
]


class _OrderItemWriteSerializer(serializers.Serializer):
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    quantity = serializers.IntegerField()

    class Meta:
        fields = ['variant', 'quantity']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
