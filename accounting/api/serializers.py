from rest_framework import serializers

from ..models import Cost, CostType, Income, ProductCost


__all__ = [
    'CostTypeSerializer', 'CostReadSerializer', 'CostWriteSerializer', 'IncomeSerializer',
    'ProductCostSerializer'
]


class CostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostType
        fields = '__all__'


class CostReadSerializer(serializers.ModelSerializer):
    type = CostTypeSerializer(read_only=True)

    class Meta:
        model = Cost
        fields = '__all__'


class CostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'


class ProductCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCost
        fields = '__all__'
