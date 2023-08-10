from rest_framework import serializers

from shop.models import *


__all__ = [
    '_BrandReadSerializer',
    '_ImageReadSerializer',
    '_AttributeValueReadSerializer',
    '_VariantForProductListSerializer',
    '_VariantSerializer',
    '_CategoryReadSerializer',
]


class _BrandReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class _ImageReadSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name='get_absolute_url')

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'product',
            'url',
            'is_main',
            'description'
        ]

    def get_absolute_url(self, obj):
        if not obj.file:
            return None
        url = obj.file.url
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(url)
        if (host := self.context.get('host')) is not None:
            return f'{host}{url}'
        return url


class _AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'title', 'description']


class _AttributeValueReadSerializer(serializers.ModelSerializer):
    attribute = _AttributeSerializer(read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = [
            'id',
            'attribute',
            'value',
            'extra_info',
            'created_at',
            'updated_at',
        ]


class _SelectorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectorType
        fields = [
            'id',
            'title',
            'code',
        ]


class _SelectorValueSerializer(serializers.ModelSerializer):
    type = _SelectorTypeSerializer(read_only=True)

    class Meta:
        model = SelectorValue
        fields = [
            'id',
            'type',
            'title',
            'value',
            'extra_info',
        ]


class _VariantForProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'selector_value',
            'is_active',
            'price',
            'inventory',
            'max_in_order',
        ]


class _VariantSerializer(serializers.ModelSerializer):
    selector_value = _SelectorValueSerializer(read_only=True)

    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'selector_value',
            'is_active',
            'price',
            'inventory',
            'max_in_order',
        ]


class _CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'selector_type']
