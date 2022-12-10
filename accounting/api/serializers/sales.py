from rest_framework import serializers

from accounting.models import *
from products.models import *


class SalesQueryParamSerializer(serializers.Serializer):
    ap_id = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        ap_id = attrs.get('ap_id')
        try:
            attrs['actual_product'] = ActualProduct.objects.get(id=ap_id)
        except ActualProduct.DoesNotExist:
            raise serializers.ValidationError(f'no actual product with id: {ap_id}')

        return attrs


class ActualProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualProduct
        fields = '__all__'


__all__ = [
    'SalesQueryParamSerializer',
    'ActualProductSerializer',
]
