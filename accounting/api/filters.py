from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from ..models import Cost, CostType


__all__ = [
    'CostTypeFilter',
]


class CostTypeFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')

    class Meta:
        model = CostType
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            title__contains=value
        )
