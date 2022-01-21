from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from ..models import *


__all__ = [
    'ActualProductFilter', 'ProductFilter', 'ProductTypeSelectorValueFilter', 'VariantFilter',
    'ProductTypeFilter', 'ProductTypeSelectorFilter', 'BrandFilter'
]


class BrandFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')

    class Meta:
        model = ActualProduct
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
            title__contains=value
        )


class ProductFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')
    is_active = filters.BooleanFilter(field_name='is_active')
    price_step = filters.NumberFilter(field_name='price_step')

    class Meta:
        model = Product
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            Q(title__contains=value) | Q(dkp=value)
        )


class ProductTypeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = ProductType
        fields = ['title']


class ProductTypeSelectorFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = ProductTypeSelector
        fields = ['title']


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
            value__contains=value
        )


class VariantFilter(filters.FilterSet):
    product_title = filters.CharFilter(field_name='product', lookup_expr='title__contains')
    search = filters.CharFilter(method='search_in_fields')
    is_active = filters.BooleanFilter(field_name='is_active')
    has_competition = filters.BooleanFilter(field_name='has_competition')

    o = OrderingFilter(
        fields=['dkpc', 'price_min', 'is_active', 'has_competition', ]
    )

    class Meta:
        model = ProductVariant
        fields = ['product', 'search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            Q(product__title__contains=value) | Q(dkpc=value)
        )
