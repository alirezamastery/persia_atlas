from rest_framework import serializers

from shop.models import Brand


__all__ = [
    'BrandReadWriteSerializer',
]


class BrandReadWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']
