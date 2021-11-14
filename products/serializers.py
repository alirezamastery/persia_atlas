from rest_framework import serializers
from .models import (Product, ProductVariant, ProductType, ProductTypeSelector,
                     ProductTypeSelectorValue, ActualProduct, Brand, Invoice, InvoiceItem)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        depth = 2


class ProductVariantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['dkpc', 'price_min', 'is_active']


class ActualProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = ActualProduct
        fields = '__all__'
        depth = 1


class BrandSerializer(serializers.ModelSerializer):
    actual_products = ActualProductSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'


class VariantSerializerDigikalaContext(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['our_stock'] = self.context['digi_data']['marketplace_seller_stock_latin']
        response['reserved'] = self.context['digi_data']['reservation_latin']
        response['warehouse_stock'] = self.context['digi_data']['warehouse_stock_latin']
        response['price'] = self.context['digi_data']['price_sale_latin']
        response['maximum_per_order'] = self.context['digi_data']['maximum_per_order_latin']
        return response


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class ProductTypeSelectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeSelector
        fields = '__all__'


class ProductTypeSelectorValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeSelectorValue
        fields = '__all__'
        depth = 1


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


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
