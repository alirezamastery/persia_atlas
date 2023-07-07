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
            'file',
            'is_main',
            'description',
        ]
