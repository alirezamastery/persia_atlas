from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from shop.models import *


__all__ = [
    'VariantSelectorValueReadSerializer',
    'ProductVariantReadSerializer',
    'ProductVariantWriteSerializer',
]


class VariantSelectorValueReadSerializer(serializers.ModelSerializer):
    class VariantSelectorTypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = VariantSelectorType
            fields = ['id', 'title', 'code']

    type = VariantSelectorTypeSerializer(read_only=True)

    class Meta:
        model = VariantSelectorValue
        fields = '__all__'


class ProductVariantReadSerializer(serializers.ModelSerializer):
    selector_value = VariantSelectorValueReadSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'product',
            'selector_value',
            'is_active',
            'price',
            'inventory',
        ]


class ProductVariantWriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.select_related('category').all())

    class Meta:
        model = ProductVariant
        fields = [
            'product',
            'selector_value',
            'price',
            'is_active',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=ProductVariant.objects.all(),
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
        return ProductVariantReadSerializer(instance).data
