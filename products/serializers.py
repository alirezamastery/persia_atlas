from rest_framework import serializers

from .models import *
from utils.logging import plogger, logger


class ProductReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        depth = 2


class BulkVariantItemSerializer(serializers.Serializer):
    dkpc = serializers.IntegerField()
    selector = serializers.PrimaryKeyRelatedField(queryset=VariantSelector.objects.all())


class ProductVariantBulkCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    actual_product = serializers.PrimaryKeyRelatedField(queryset=ActualProduct.objects.all())
    price_min = serializers.IntegerField()
    is_active = serializers.BooleanField()
    variants = BulkVariantItemSerializer(many=True)

    def validate(self, attrs):
        variants = attrs['variants']
        dkpc_list = [v['dkpc'] for v in variants]
        duplicate_variants = ProductVariant.objects.filter(dkpc__in=dkpc_list)
        if duplicate_variants.count() > 0:
            txt = ', '.join(str(v.dkpc) for v in duplicate_variants)
            raise serializers.ValidationError(f'dkpc already exists: {txt}')

        product = attrs['product']
        duplicate_selectors = []
        existing_selectors = product.variants.all().values_list('selector_id', flat=True)
        for variant in variants:
            if variant['selector'].id in existing_selectors:
                duplicate_selectors.append(variant['selector'].value)
        if len(duplicate_selectors) > 0:
            txt = ', '.join(value for value in duplicate_selectors)
            raise serializers.ValidationError(
                f'product variant with selector: {txt} already exists'
            )

        return attrs

    def create(self, validated_data):
        product = validated_data['product']
        actual_product = validated_data['actual_product']
        price_min = validated_data['price_min']
        is_active = validated_data['is_active']
        variants = validated_data['variants']
        objs = [
            ProductVariant(
                product=product,
                actual_product=actual_product,
                price_min=price_min,
                is_active=is_active,
                dkpc=variant['dkpc'],
                selector=variant['selector']
            )
            for variant in variants
        ]
        created_objs = ProductVariant.objects.bulk_create(objs)
        return created_objs


class ProductVariantWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        exclude = ['has_competition']


class ActualProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = ActualProduct
        fields = '__all__'
        depth = 1


class ActualProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualProduct
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    # actual_products = ActualProductSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'


class ProductTypeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'
        depth = 1


class ProductTypeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['title', 'selector_type']


class VariantSelectorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantSelectorType
        fields = '__all__'
        depth = 1


class VariantSelectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantSelector
        fields = '__all__'
        depth = 1


class VariantSerializerDigikalaContext(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['dk'] = self.context['digi_data']
        return response


class DKPCListSerializer(serializers.Serializer):
    dkpc_list = serializers.ListField(child=serializers.CharField(), allow_empty=False)

    def validate(self, data):
        dkpc_list = data.get('dkpc_list')
        for dkpc in dkpc_list:
            if not ProductVariant.objects.filter(dkpc=dkpc).exists():
                raise serializers.ValidationError(f'no variant whit dkpc {dkpc} found id database')
        return data


class UpdateVariantDigiDataSerializer(serializers.Serializer):
    price = serializers.IntegerField(required=False)
    seller_stock = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)


class UpdateVariantStatusSerializer(serializers.Serializer):
    dkpc = serializers.CharField()
    is_active = serializers.BooleanField()


class UpdateBrandStatusSerializer(serializers.Serializer):
    id = serializers.CharField()
    is_active = serializers.BooleanField()

    @staticmethod
    def validate_id(value):
        if not Brand.objects.filter(id=value).exists():
            raise serializers.ValidationError(f'no brand with id: {value}')
        return value


class RobotStatusSerializer(serializers.Serializer):
    robot_is_on = serializers.BooleanField(required=True)

    class Meta:
        fields = '__all__'


class ScrapeInvoiceSerializer(serializers.Serializer):
    row_number = serializers.IntegerField(default=1, min_value=1, max_value=10)

    class Meta:
        fields = '__all__'


class ToggleVariantStatusSerializer(serializers.Serializer):
    actual_product_id = serializers.IntegerField()
    selector_ids = serializers.ListSerializer(child=serializers.IntegerField(), allow_empty=False)
    is_active = serializers.BooleanField()


__all__ = [
    'UpdateVariantDigiDataSerializer',
    'UpdateVariantStatusSerializer',
    'VariantSerializerDigikalaContext',
    'ActualProductSerializer',
    'BrandSerializer',
    'ProductVariantSerializer',
    'ProductReadSerializer',
    'ProductWriteSerializer',
    'ProductVariantWriteSerializer',
    'VariantSelectorSerializer',
    'VariantSelectorTypeSerializer',
    'ProductTypeReadSerializer',
    'ProductTypeWriteSerializer',
    'ActualProductWriteSerializer',
    'UpdateBrandStatusSerializer',
    'RobotStatusSerializer',
    'ScrapeInvoiceSerializer',
    'ProductVariantBulkCreateSerializer',
    'ToggleVariantStatusSerializer',
]
