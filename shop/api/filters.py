from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from shop.models import *


__all__ = [
    'ProductAttributeFilter',
    'ProductFilter',
    'VariantSelectorTypeFilter',
    'VariantFilter',
]

class ProductAttributeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Attribute
        fields = ['search']


class ProductFilter(filters.FilterSet):
    q = filters.CharFilter(method='search_in_fields')
    maxp = filters.NumberFilter(field_name='price', lookup_expr='gte')
    minp = filters.NumberFilter(field_name='price', lookup_expr='lte')
    has_inv = filters.BooleanFilter(method='has_inentory')

    class Meta:
        model = Product
        fields = ['q', 'maxp', 'minp']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(brand__title=value))

    def has_inentory(self, qs, name, value):
        return qs.filter(total_inventory__gt=0)


class VariantSelectorTypeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = SelectorType
        fields = ['search']

