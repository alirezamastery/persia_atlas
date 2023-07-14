from rest_framework import serializers

from shop.models import ProductAttribute


__all__ = [
    'ProductAttributeReadWriteSerializer',
]


class ProductAttributeReadWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'title', 'description']
