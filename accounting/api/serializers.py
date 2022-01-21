from rest_framework import serializers

from ..models import Cost, CostType


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