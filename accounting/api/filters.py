from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from ..models import *


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

    o = OrderingFilter(fields=['date', 'amount'])

    class Meta:
        model = Cost
        fields = '__all__'

    @staticmethod
    def search_in_fields(qs, name, value):
        return qs.filter(
            type__title__contains=value
        )


class IncomeFilter(filters.FilterSet):
    date_gte = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_lte = filters.DateFilter(field_name='date', lookup_expr='lte')

    o = OrderingFilter(fields=['date', 'amount'])

    class Meta:
        model = Income
        fields = ['date_gte', 'date_lte']


class ProductCostFilter(filters.FilterSet):
    date_gte = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_lte = filters.DateFilter(field_name='date', lookup_expr='lte')

    o = OrderingFilter(fields=['date', 'amount'])

    class Meta:
        model = ProductCost
        fields = ['date_gte', 'date_lte']


class InvoiceFilter(filters.FilterSet):
    # number = filters.CharFilter(method='search_in_fields')
    start_date_gte = filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date_lte = filters.DateFilter(field_name='start_date', lookup_expr='lte')

    end_date_gte = filters.DateFilter(field_name='end_date', lookup_expr='gte')
    end_date_lte = filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Invoice
        fields = ['number', 'start_date_gte', 'start_date_lte', 'end_date_gte', 'end_date_lte']


__all__ = [
    'CostTypeFilter',
    'CostFilter',
    'IncomeFilter',
    'ProductCostFilter',
    'InvoiceFilter'
]
