from rest_framework import serializers

from shop.models import Brand


__all__ = [
    'BrandSerializer',
]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['user', 'items']
