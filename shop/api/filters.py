from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from shop.models import *


__all__ = [
    'ProductCategoryFilter',
    'ProductAttributeFilter',
    'ProductFilter',
    'VariantSelectorTypeFilter',
    'ProductVariantFilter',
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


class ProductFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')
    is_active = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Product
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(brand__title=value))


class VariantSelectorTypeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = VariantSelectorType
        fields = ['search']


class ProductVariantFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')
    is_active = filters.BooleanFilter(field_name='is_active')

    o = OrderingFilter(fields=['price', 'is_active'])

    class Meta:
        model = ProductVariant
        fields = ['search', 'is_active']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(product__title__icontains=value) | Q(selector_value__title=value))
