from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from shop.models import *


__all__ = [
    'ProductCategoryListSerializer',
    'ProductCategoryDetailSerializer',
]


class _AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'title', 'description']


class ProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'selector_type']


class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    parent_node_id = serializers.SerializerMethodField('get_parent_node_id')
    attributes = serializers.SerializerMethodField('get_attributes')

    class Meta:
        model = Category
        fields = ['id', 'title', 'selector_type', 'parent_node_id', 'attributes']

    @extend_schema_field(OpenApiTypes.INT)
    def get_parent_node_id(self, obj: Category):
        parent_node = obj.get_parent()
        return parent_node.id if parent_node is not None else 0

    @extend_schema_field(_AttributeSerializer)
    def get_attributes(self, obj: Category):
        attribute_ids = CategoryAttribute.objects \
            .filter(category=obj) \
            .select_related('attribute') \
            .values_list('attribute_id', flat=True)
        attributes = Attribute.objects.filter(id__in=attribute_ids)
        return _AttributeSerializer(attributes, many=True).data
