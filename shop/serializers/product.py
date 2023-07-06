from rest_framework import serializers

from .category import *
from shop.models import *
from shop.queries import get_product_with_attrs


__all__ = [
    'BrandSerializer',
    'ProductAttributeSerializer',
    'ProductAttributeValueReadSerializer',
    'ProductDetailSerializer',
    'ProductListSerializer',
    'ProductAttributeValueWriteSerializer',
    'ProductWriteSerializer',
]

from .variants import ProductVariantReadSerializer


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'url', 'is_main', 'description']


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = ProductCategoryReadSerializer(read_only=True)
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'is_active',
            'slug',
            'category',
            'images',
        ]


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductAttributeValueReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    attribute = ProductAttributeSerializer(read_only=True)
    value = serializers.CharField()

    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'attribute', 'value']


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = ProductCategoryReadSerializer(read_only=True)
    attribute_values = ProductAttributeValueReadSerializer(read_only=True, many=True)
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'is_active',
            'slug',
            'category',
            'attribute_values',
            'images',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)

        if self.context.get('is_retrieve') is True:
            variants = ProductVariant.objects.select_related('selector_value').filter(product=instance)
            response['variants'] = ProductVariantReadSerializer(variants, many=True).data

            images = instance.images.all().order_by('-is_main')
            response['images'] = ImageSerializer(images, many=True).data

        if self.context.get('is_list') is True:
            main_img = instance.images.filter(is_main=True).first()
            if main_img is not None:
                response['main_img'] = ImageSerializer(main_img).data

        return response


class ProductAttributeValueWriteSerializer(serializers.Serializer):
    attribute = serializers.PrimaryKeyRelatedField(queryset=ProductAttribute.objects.all())
    value = serializers.CharField()

    class Meta:
        fields = ['attribute', 'value']


class NewProductImageWriteSerializer(serializers.Serializer):
    file = serializers.CharField()
    is_main = serializers.BooleanField()


class ProductWriteSerializer(serializers.ModelSerializer):
    attribute_values = serializers.ListSerializer(
        child=ProductAttributeValueWriteSerializer(),
        allow_empty=True
    )
    new_images = serializers.ListSerializer(child=NewProductImageWriteSerializer(), allow_empty=True)
    main_img = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), required=False)

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
            category_attrs = ProductCategoryAttribute.objects \
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
        # don't change the category after product creation!
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
            main_img.is_main = True
            main_img.save()

        new_images = self.validated_data.get('new_images')
        print(f'{new_images = }')
        for img in new_images:
            print(f'{img = }')
            url = img['file']
            is_main = img['is_main']
            if url.startswith('/media/'):
                url = url.replace('/media/', '/', 1)
            ProductImage.objects.create(url=url, product=product, is_main=is_main)

        return product

    def to_representation(self, instance):
        return ProductDetailSerializer(instance).data
