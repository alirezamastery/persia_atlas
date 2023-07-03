from rest_framework import serializers

from shop.models import *


__all__ = [
    'ProductCategoryReadSerializer',
    'ProductCategoryWriteSerializer',
]


class ProductCategoryReadSerializer(serializers.ModelSerializer):
    class AttributeSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductAttribute
            fields = '__all__'

    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'selector_type']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if self.context.get('with_details'):
            parent_node = instance.get_parent()
            response['parent_node_id'] = parent_node.id if parent_node is not None else None
            attribute_ids = ProductCategoryAttribute.objects \
                .filter(category=instance) \
                .select_related('attribute') \
                .values_list('id', flat=True)
            attributes = ProductAttribute.objects.filter(id__in=attribute_ids)
            response['attributes'] = self.AttributeSerializer(attributes, many=True).data

        return response


class ProductCategoryWriteSerializer(serializers.Serializer):
    title = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), allow_null=True)
    selector_type = serializers.PrimaryKeyRelatedField(queryset=VariantSelectorType.objects.all())
    attributes = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=ProductAttribute.objects.all()),
        allow_empty=True,
        default=[]
    )

    class Meta:
        fields = ['title', 'parent', 'attributes']

    def create(self, validated_data):
        parent_node = validated_data['parent']
        child_data = {
            'title': validated_data['title']
        }
        if parent_node is None:
            category = ProductCategory.add_root(**child_data)
        else:
            category = parent_node.add_child(**child_data)

        for attribute in validated_data['attributes']:
            ProductCategoryAttribute.objects.create(category=category, attribute=attribute)

        return category

    def update(self, category, validated_data):
        category.title = validated_data.get('title', category.title)
        category.save()

        parent_node = validated_data.get('parent', -1)
        if parent_node != -1:
            if parent_node is None:
                category.move(ProductCategory.get_first_root_node(), pos='sorted-sibling')
            elif not parent_node.id == category.id:
                category.move(parent_node, pos='sorted-child')

        current_attrs = ProductCategoryAttribute.objects.filter(category=category)
        current_attr_ids = set([attr.id for attr in current_attrs])
        request_attr_ids = set([attr.id for attr in validated_data.get('attributes', [])])
        new_attr_ids = request_attr_ids - current_attr_ids
        for new_attr_id in new_attr_ids:
            ProductCategoryAttribute.objects.create(category=category, attribute_id=new_attr_id)

            product_attr_objs = []
            for product in category.products.all():
                print('product:', product)
                product_attr_objs.append(
                    ProductAttributeValue(product=product, attribute_id=new_attr_id, value='')
                )
            ProductAttributeValue.objects.bulk_create(product_attr_objs)

        return category

    def to_representation(self, category):
        return ProductCategoryReadSerializer(category).data
