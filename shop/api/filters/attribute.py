from django_filters import rest_framework as filters

from shop.models import *


__all__ = [
    'AttributeFilter',
]


class AttributeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Attribute
        fields = ['search']
