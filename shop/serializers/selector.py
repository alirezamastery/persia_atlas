from rest_framework import serializers

from ..models import *


__all__ = [
    'VariantSelectorValueReadSerializer',
    'VariantSelectorTypeReadSerializer',
]


class VariantSelectorValueReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantSelectorValue
        fields = ['id', 'type', 'title', 'value', 'extra_info']


class VariantSelectorTypeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantSelectorType
        fields = [
            'id',
            'title',
            'code',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        values = VariantSelectorValue.objects.filter(type=instance)
        response['values'] = VariantSelectorValueReadSerializer(values, many=True).data
        return response
