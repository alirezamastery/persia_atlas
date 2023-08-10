from rest_framework import serializers

from shop.models import *


__all__ = [
    'ProductCategoryReadSerializer',
]


class ProductCategoryReadSerializer(serializers.ModelSerializer):
    class AttributeSerializer(serializers.ModelSerializer):
        class Meta:
            model = Attribute
            fields = '__all__'

    class Meta:
        model = Category
        fields = ['id', 'title', 'selector_type']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if self.context.get('with_details'):
            parent_node = instance.get_parent()
            response['parent_node_id'] = parent_node.id if parent_node is not None else 0
            attribute_ids = CategoryAttribute.objects \
                .filter(category=instance) \
                .select_related('attribute') \
                .values_list('attribute_id', flat=True)
            attributes = Attribute.objects.filter(id__in=attribute_ids)
            response['attributes'] = self.AttributeSerializer(attributes, many=True).data

        return response
