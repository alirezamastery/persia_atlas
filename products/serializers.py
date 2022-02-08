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


class ProductVariantWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        exclude = ['has_competition', 'selector_values']


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
    actual_products = ActualProductSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'
        depth = 1


class ProductTypeSelectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeSelector
        fields = '__all__'
        depth = 1


class ProductTypeSelectorValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeSelectorValue
        fields = '__all__'
        depth = 1


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'


class VariantSerializerDigikalaContext(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['is_digi_active'] = self.context['digi_data']['isActive']
        response['our_stock'] = self.context['digi_data']['marketplace_seller_stock_latin']
        response['reserved'] = self.context['digi_data']['reservation_latin']
        response['warehouse_stock'] = self.context['digi_data']['warehouse_stock_latin']
        response['price'] = self.context['digi_data']['price_sale_latin']
        response['maximum_per_order'] = self.context['digi_data']['maximum_per_order_latin']
        response['image_src'] = self.context['digi_data']['image_src']
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
    dkpc = serializers.CharField()
    price = serializers.IntegerField()
    our_stock = serializers.IntegerField()


class UpdateVariantStatusSerializer(serializers.Serializer):
    dkpc = serializers.CharField()
    is_active = serializers.BooleanField()


class UpdateVariantPriceMinSerializer(serializers.Serializer):
    dkpc = serializers.CharField()
    price_min = serializers.IntegerField()


__all__ = [
    'UpdateVariantPriceMinSerializer',
    'UpdateVariantDigiDataSerializer',
    'UpdateVariantStatusSerializer',
    'VariantSerializerDigikalaContext',
    'ActualProductSerializer',
    'BrandSerializer',
    'ProductVariantSerializer',
    'InvoiceSerializer',
    'InvoiceItemSerializer',
    'ProductReadSerializer',
    'ProductWriteSerializer',
    'ProductVariantWriteSerializer',
    'ProductTypeSelectorValueSerializer',
    'ProductTypeSelectorSerializer',
    'ProductTypeSerializer',
    'ActualProductWriteSerializer',
]
