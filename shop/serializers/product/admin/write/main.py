from rest_framework import serializers

from shop.models import *
from shop.queries import get_product_with_attrs
from shop.serializers.product.admin.read import ProductDetailSerializerAdmin
from .sub import *


__all__ = [
    'ProductWriteSerializerAdmin',
]


class ProductWriteSerializerAdmin(serializers.ModelSerializer):
    attribute_values = serializers.ListSerializer(child=_ProductAttributeValueWriteSerializer(), allow_empty=True)
    new_images = serializers.ListSerializer(child=_NewProductImageWriteSerializer(), allow_empty=True)
    main_img = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'brand',
            'title',
            'description',
            'is_active',
            'category',
            'attribute_values',
            'new_images',
            'main_img',
        ]

    def validate(self, attrs):
        category = attrs.get('category')
        if category is not None:
            category_attrs = CategoryAttribute.objects \
                .filter(category=category) \
                .values_list('attribute_id', flat=True)
            category_attrs = set(category_attrs)
            print(f'{category_attrs = }')
            attribute_values = attrs.get('attribute_values', [])
            attribute_value_ids = set([a['attribute'].id for a in attribute_values])
            print(f'{attribute_value_ids = }')
            if attribute_value_ids != category_attrs:
                missing_attrs = category_attrs - attribute_value_ids
                raise serializers.ValidationError(
                    f'these attributes are required: {list(missing_attrs)}',
                    code="missing_attrs"
                )
        print('validate attrs:', attrs)
        return attrs

    def create(self, validated_data):
        print('*' * 150)
        print(f'{validated_data = }')
        attribute_values = validated_data.pop('attribute_values')

        product = Product.objects.create(
            brand=validated_data['brand'],
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            is_active=validated_data.get('is_active', True),
            category=validated_data['category'],
        )
        print(f'{product = }')

        for attr_value in attribute_values:
            ProductAttributeValue.objects.create(
                product=product,
                attribute=attr_value['attribute'],
                value=attr_value['value']
            )

        product = get_product_with_attrs(product.id)

        return product

    def update(self, instance, validated_data):
        instance.brand = validated_data.get('brand', instance.brand)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        # Don't change the category after product creation!
        # instance.category = validated_data.get('category', instance.category)
        instance.save()

        attribute_values = validated_data.pop('attribute_values')
        for av in attribute_values:
            print('attr:', av)
            try:
                attr = ProductAttributeValue.objects.get(product=instance, attribute=av['attribute'])
                attr.value = av['value']
                attr.save()
            except ProductAttributeValue.DoesNotExist:
                ProductAttributeValue.objects.create(
                    product=instance,
                    attribute=av['attribute'],
                    value=av['value']
                )

        product = get_product_with_attrs(instance.id)

        return product

    def save(self, **kwargs):
        product = super().save(**kwargs)

        main_img = self.validated_data.get('main_img', None)
        print(f'{main_img = }')
        if main_img is not None:
            print(f'file: {main_img.file}')
            main_img.is_main = True
            main_img.save()
            product.thumbnail = main_img.file
            product.save()

        new_images = self.validated_data.get('new_images')
        print(f'{new_images = }')
        for img in new_images:
            print(f'{img = }')
            file = img['file']
            is_main = img['is_main']
            if file.startswith('/media/'):
                file = file.replace('/media/', '/', 1)
            ProductImage.objects.create(file=file, product=product, is_main=is_main)
            if is_main:
                product.thumbnail = file
                product.save()

        return product

    def to_representation(self, instance):
        return ProductDetailSerializerAdmin(instance).data
