from rest_framework import serializers
from .models import (Product, ProductVariant, ProductType, ProductTypeSelector, ProductTypeSelectorValue, ActualProduct)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        depth = 2


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


class ActualProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = ActualProduct
        fields = '__all__'
