from rest_framework import serializers

from shop.models import *


__all__ = [
    '_ProductAttributeValueWriteSerializer',
    '_NewProductImageWriteSerializer',
]


class _ProductAttributeValueWriteSerializer(serializers.Serializer):
    attribute = serializers.PrimaryKeyRelatedField(queryset=ProductAttribute.objects.all())
    value = serializers.CharField()

    class Meta:
        fields = ['attribute', 'value']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class _NewProductImageWriteSerializer(serializers.Serializer):
    file = serializers.CharField()
    is_main = serializers.BooleanField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
