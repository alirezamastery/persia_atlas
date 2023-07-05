from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from shop.models import *


__all__ = [
    'ProductCategoryFilter',
    'ProductAttributeFilter',
    'VariantSelectorTypeFilter',
]


class ProductCategoryFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = ['search']


class ProductAttributeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = ProductAttribute
        fields = ['search']


class VariantSelectorTypeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = VariantSelectorType
        fields = ['search']
