from rest_framework import serializers

from ..models import *


__all__ = [
    'ImageReadSerializer',
]


class ImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'id',
            'product',
            'url',
            'is_main',
            'description',
        ]
