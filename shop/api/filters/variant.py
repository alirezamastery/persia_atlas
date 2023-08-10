from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from shop.models import *


__all__ = [
    'VariantFilter',
]


class VariantFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')
    is_active = filters.BooleanFilter(field_name='is_active')

    o = OrderingFilter(fields=['price', 'is_active'])

    class Meta:
        model = Variant
        fields = ['search', 'is_active']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(product__title__icontains=value) | Q(selector_value__title=value))
