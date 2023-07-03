from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from shop.models import *


__all__ = [
    'VariantSelectorTypeSerializer',
    'VariantSelectorValueReadSerializer',
    'VariantSelectorValueWriteSerializer',
    'ProductVariantReadSerializer',
    'ProductVariantWriteSerializer',
]


class VariantSelectorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantSelectorType
        fields = '__all__'


class VariantSelectorValueReadSerializer(serializers.ModelSerializer):
    type = VariantSelectorTypeSerializer(read_only=True)

    class Meta:
        model = VariantSelectorValue
        fields = '__all__'


class VariantSelectorValueWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantSelectorValue
        fields = ['type', 'value', 'extra_info']


class ProductVariantReadSerializer(serializers.ModelSerializer):
    selector_value = VariantSelectorValueReadSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'product',
            'selector_value',
            'price',
            'is_active',
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
