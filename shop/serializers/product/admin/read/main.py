from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from shop.models import *
from .sub import *


__all__ = [
    'ProductListSerializerAdmin',
    'ProductDetailSerializerAdmin',
]


class ProductListSerializerAdmin(serializers.ModelSerializer):
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
            'variants',
            'created_at',
            'updated_at'
        ]


class ProductDetailSerializerAdmin(serializers.ModelSerializer):
    brand = _BrandReadSerializer(read_only=True)
    category = _CategoryReadSerializer(read_only=True)
    attribute_values = _AttributeValueReadSerializer(read_only=True, many=True)
    variants = _VariantSerializer(read_only=True, many=True)
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
            'created_at',
            'updated_at'
        ]

    @extend_schema_field(_ImageReadSerializer)
    def get_images(self, obj: Product):
        images = obj.images.all().order_by('-is_main')
        return _ImageReadSerializer(images, many=True, context=self.context).data
