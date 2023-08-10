from rest_framework import serializers

from shop.models import Attribute


__all__ = [
    'AttributeReadWriteSerializer',
]


class AttributeReadWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'title', 'description']
