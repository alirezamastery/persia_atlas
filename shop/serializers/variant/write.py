from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from shop.models import *
from .read import VariantReadSerializer


__all__ = [
    'VariantCreateSerializer',
    'VariantUpdateSerializer',
]


class VariantCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.select_related('category').all())

    class Meta:
        model = Variant
        fields = [
            'product',
            'selector_value',
            'is_active',
            'price',
            'inventory',
            'max_in_order',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Variant.objects.all(),
                fields=['product', 'selector_value']
            )
        ]

    def validate(self, attrs):
        product = attrs['product']
        selector_value = attrs['selector_value']

        selector_type_id = product.category.selector_type_id
        if selector_value.type_id != selector_type_id:
            raise serializers.ValidationError(f'the selector type id must be: {selector_type_id}')

        return attrs

    def to_representation(self, instance):
        return VariantReadSerializer(instance).data


class VariantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['is_active', 'price', 'inventory', 'max_in_order']
