from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from shop.models import *
from .sub import *


__all__ = [
    'ProductDetailSerializer',
    'ProductListSerializer',
]


class ProductListSerializer(serializers.ModelSerializer):
    brand = _BrandReadSerializer(read_only=True)
    category = _CategoryReadSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'is_active',
            'slug',
            'thumbnail',
            'category',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = _BrandReadSerializer(read_only=True)
    category = _CategoryReadSerializer(read_only=True)
    attribute_values = _AttributeValueReadSerializer(read_only=True, many=True)
    variants = serializers.SerializerMethodField(method_name='get_variants')
    images = serializers.SerializerMethodField(method_name='get_images')

    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'is_active',
            'slug',
            'thumbnail',
            'category',
            'attribute_values',
            'variants',
            'images',
        ]

    @extend_schema_field(_VariantSerializer)
    def get_variants(self, obj: Product):
        variants = ProductVariant.objects.select_related('selector_value__type').filter(product=obj)
        return _VariantSerializer(variants, many=True).data

    @extend_schema_field(_ImageReadSerializer)
    def get_images(self, obj: Product):
        images = obj.images.all().order_by('-is_main')
        return _ImageReadSerializer(images, many=True, context=self.context).data
