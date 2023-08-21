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
    pmin = filters.NumberFilter(field_name='price_min', lookup_expr='gte')
    pmax = filters.NumberFilter(field_name='price_min', lookup_expr='lte')
    # pmin = filters.NumberFilter(method='price_min_filter')
    # pmax = filters.NumberFilter(method='price_max_filter')
    is_av = filters.BooleanFilter(method='is_available')

    o = CustomOrderingFilter(fields=['n', 'p', '-p', 'l'])  # map: newest price -price liked

    class Meta:
        model = Product
        fields = ['q', 'pmax', 'pmin', 'is_av']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(brand__title=value))

    def is_available(self, qs, name, value):
        if value:
            return qs.filter(total_inventory__gt=0)
        return qs

    def price_min_filter(self, qs, name, value):
        if value > -1:
            return qs.filter(price_min__gte=value)
        return qs

    def price_max_filter(self, qs, name, value):
        if value > -1:
            return qs.filter(price_min__lte=value)
        return qs


class ProductFilterAdmin(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')
    pmax = filters.NumberFilter(field_name='price_min', lookup_expr='gte')
    pmin = filters.NumberFilter(field_name='price_min', lookup_expr='lte')
    has_inv = filters.BooleanFilter(method='has_inventory')

    class Meta:
        model = Product
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(brand__title=value))

    def has_inventory(self, qs, name, value):
        return qs.filter(total_inventory__gt=0)
