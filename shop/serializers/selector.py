from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from ..models import *


__all__ = [
    'VariantSelectorTypeReadSerializer',
]


class _VariantSelectorValueReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantSelectorValue
        fields = ['id', 'type', 'title', 'value', 'extra_info']


class VariantSelectorTypeReadSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField(method_name='get_values')

    class Meta:
        model = VariantSelectorType
        fields = [
            'id',
            'title',
            'code',
            'values',
        ]

    @extend_schema_field(_VariantSelectorValueReadSerializer)
    def get_values(self, obj: VariantSelectorType):
        values = VariantSelectorValue.objects.filter(type=obj)
        return _VariantSelectorValueReadSerializer(values, many=True).data
