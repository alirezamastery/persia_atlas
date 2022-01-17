from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from ..models import Cost, CostType


__all__ = [
    'CostTypeFilter', 'CostFilter'
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


class CostFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')
    date_gte = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_lte = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Cost
        fields = '__all__'

    @staticmethod
    def search_in_fields(qs, name, value):
        return qs.filter(
            type__title__contains=value
        )
