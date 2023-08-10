from django_filters import rest_framework as filters

from shop.models import *


__all__ = [
    'CategoryFilter',
]


class CategoryFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['search']
