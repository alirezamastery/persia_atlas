from rest_framework import serializers

from shop.models import *


__all__ = [
    '_ProductSerializer',
    '_VariantSelectorValueReadSerializer',
]


class _ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'is_active',
            'slug',
            'category',
        ]


class _VariantSelectorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantSelectorType
        fields = ['id', 'title', 'code']


class _VariantSelectorValueReadSerializer(serializers.ModelSerializer):
    type = _VariantSelectorTypeSerializer(read_only=True)

    class Meta:
        model = VariantSelectorValue
        fields = ['id', 'type', 'title', 'value', 'extra_info']
