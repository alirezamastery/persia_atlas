from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter
from django_filters.constants import EMPTY_VALUES

from shop.models import *


__all__ = [
    'ProductFilterPublic',
    'ProductFilterAdmin',
]


class CustomOrderingFilter(OrderingFilter):

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        val = value[0]
        if val == 'n':
            return qs.order_by('-created_at')
        elif val == 'p':
            return qs.order_by('price_min')
        elif val == '-p':
            return qs.order_by('-price_min')
        elif val == 'l':
            return qs.order_by('-created_at')

        return qs


class ProductFilterPublic(filters.FilterSet):
    q = filters.CharFilter(method='search_in_fields')
    maxp = filters.NumberFilter(field_name='price', lookup_expr='gte')
    minp = filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_av = filters.BooleanFilter(method='is_available')

    o = CustomOrderingFilter(fields=['n', 'p', '-p', 'l'])  # map: newest price -price liked

    class Meta:
        model = Product
        fields = ['q', 'maxp', 'minp', 'is_av']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(brand__title=value))

    def is_available(self, qs, name, value):
        return qs.filter(total_inventory__gt=0)


class ProductFilterAdmin(filters.FilterSet):
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
