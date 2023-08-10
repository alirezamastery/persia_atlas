from django_filters import rest_framework as filters

from shop.models import *


__all__ = [
    'BrandFilter',
]


class BrandFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Brand
        fields = ['search']
