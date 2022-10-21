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


class VariantSelectorTypeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = VariantSelectorType
        fields = ['search']


class VariantSelectorFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')

    o = OrderingFilter(
        fields=['digikala_id', 'value']
    )

    class Meta:
        model = VariantSelector
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
    selector_id = filters.NumberFilter(field_name='selector')
    actual_product_id = filters.NumberFilter(field_name='actual_product')

    o = OrderingFilter(fields=['dkpc', 'price_min', 'is_active', 'has_competition'])

    class Meta:
        model = ProductVariant
        fields = ['is_active', 'search', 'has_competition']

    def search_in_fields(self, qs, name, value):
        if value.isdigit():
            return qs.filter(
                Q(product__title__icontains=value) | Q(dkpc=value)
            )
        return qs.filter(
            product__title__icontains=value
        )


__all__ = [
    'ActualProductFilter',
    'ProductFilter',
    'VariantSelectorFilter',
    'VariantFilter',
    'ProductTypeFilter',
    'VariantSelectorTypeFilter',
    'BrandFilter',
]
