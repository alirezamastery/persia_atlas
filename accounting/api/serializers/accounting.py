from rest_framework import serializers

from accounting.models import *


__all__ = [
    'CostTypeSerializer',
    'CostReadSerializer',
    'CostWriteSerializer',
    'IncomeSerializer',
    'ProductCostSerializer',
    'JalaliDateSerializer',
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
        fields = ['type', 'amount', 'date', 'description']


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'


class ProductCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCost
        fields = '__all__'


class JalaliDateSerializer(serializers.Serializer):
    j_month = serializers.IntegerField(min_value=1, max_value=12)
    j_year = serializers.IntegerField()
