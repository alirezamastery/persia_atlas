from rest_framework import serializers

from shop.models import *


__all__ = [
    'ProductCategoryReadSerializer',
]


class _AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'title', 'description']


class ProductCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'selector_type']

    def to_representation(self, instance):
        response = super().to_representation(instance)

        if self.context.get('with_details'):
            parent_node = instance.get_parent()
            response['parent_node_id'] = parent_node.id if parent_node is not None else 0
            attribute_ids = ProductCategoryAttribute.objects \
                .filter(category=instance) \
                .select_related('attribute') \
                .values_list('attribute_id', flat=True)
            attributes = ProductAttribute.objects.filter(id__in=attribute_ids)
            response['attributes'] = _AttributeSerializer(attributes, many=True).data

        return response
