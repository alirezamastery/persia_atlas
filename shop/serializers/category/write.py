from rest_framework import serializers

from shop.models import *
from .read import ProductCategoryDetailSerializer


__all__ = [
    'ProductCategoryWriteSerializer',
]


class ProductCategoryWriteSerializer(serializers.Serializer):
    title = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    selector_type = serializers.PrimaryKeyRelatedField(queryset=SelectorType.objects.all())
    attributes = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all()),
        allow_empty=True,
        default=[]
    )

    class Meta:
        fields = ['title', 'parent', 'attributes']

    def create(self, validated_data):
        parent_node = validated_data['parent']
        child_data = {
            'title':         validated_data['title'],
            'selector_type': validated_data['selector_type']
        }
        if parent_node is None:
            category = Category.add_root(**child_data)
        else:
            category = parent_node.add_child(**child_data)

        attr_ids = set(attr.id for attr in validated_data['attributes'])
        for attr_id in attr_ids:
            CategoryAttribute.objects.create(category=category, attribute_id=attr_id)

        return category

    def update(self, category, validated_data):
        category.title = validated_data.get('title', category.title)
        category.save()

        parent_node = validated_data.get('parent', -1)
        if parent_node != -1:
            if parent_node is None:
                category.move(Category.get_first_root_node(), pos='sorted-sibling')
            elif not parent_node.id == category.id:
                category.move(parent_node, pos='sorted-child')

        current_attrs = CategoryAttribute.objects.filter(category=category)
        current_attr_ids = set(attr.attribute_id for attr in current_attrs)
        request_attr_ids = set(attr.id for attr in validated_data.get('attributes', []))
        new_attr_ids = request_attr_ids - current_attr_ids
        removed_attr_ids = current_attr_ids - request_attr_ids

        for new_attr_id in new_attr_ids:
            CategoryAttribute.objects.create(category=category, attribute_id=new_attr_id)

            product_attr_objs = []
            for product in category.products.all():
                product_attr_objs.append(
                    ProductAttributeValue(product=product, attribute_id=new_attr_id, value='')
                )
            ProductAttributeValue.objects.bulk_create(product_attr_objs)

        for removed_attr_id in removed_attr_ids:
            try:
                CategoryAttribute.objects.get(attribute_id=removed_attr_id).delete()
            except CategoryAttribute.DoesNotExist:
                pass
            for product in category.products.all():
                try:
                    ProductAttributeValue.objects.get(attribute_id=removed_attr_id, product=product).delete()
                except ProductAttributeValue.DoesNotExist:
                    pass

        return category

    def to_representation(self, category):
        return ProductCategoryDetailSerializer(category).data
