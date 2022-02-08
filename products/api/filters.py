from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from ..models import *


class BrandFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')

    class Meta:
        model = Brand
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            title__icontains=value
        )


class ActualProductFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')

    class Meta:
        model = ActualProduct
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            title__icontains=value
        )


class ProductFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')
    is_active = filters.BooleanFilter(field_name='is_active')
    price_step = filters.NumberFilter(field_name='price_step')

    class Meta:
        model = Product
        fields = ['search', 'is_active', 'price_step']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(dkp=value)
        )


class ProductTypeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = ProductType
        fields = ['search']


class ProductTypeSelectorFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = ProductTypeSelector
        fields = ['search']


class ProductTypeSelectorValueFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')

    o = OrderingFilter(
        fields=['digikala_id', 'value']
    )

    class Meta:
        model = ProductTypeSelectorValue
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            value__icontains=value
        )


class VariantFilter(filters.FilterSet):
    product_title = filters.CharFilter(field_name='product', lookup_expr='title__icontains')
    search = filters.CharFilter(method='search_in_fields')
    is_active = filters.BooleanFilter(field_name='is_active')
    has_competition = filters.BooleanFilter(field_name='has_competition')
    selector_id = filters.NumberFilter(field_name='selector', lookup_expr='selector__id')

    o = OrderingFilter(fields=['dkpc', 'price_min', 'is_active', 'has_competition'])

    class Meta:
        model = ProductVariant
        fields = ['is_active', 'search', 'has_competition']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            Q(product__title__icontains=value) | Q(dkpc=value)
        )


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
    'ActualProductFilter',
    'ProductFilter',
    'ProductTypeSelectorValueFilter',
    'VariantFilter',
    'ProductTypeFilter',
    'ProductTypeSelectorFilter',
    'BrandFilter',
    'InvoiceFilter'
]
