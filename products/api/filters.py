from django.db.models import Q
from django_filters import rest_framework as filters

from ..models import Product, ActualProduct, ProductVariant, ProductTypeSelectorValue


__all__ = ['ActualProductFilter', 'ProductFilter', 'ProductTypeSelectorValueFilter', 'VariantFilter', ]


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

    class Meta:
        model = Product
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            Q(title__contains=value) | Q(dkp=value)
        )


class ProductTypeSelectorValueFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_in_fields')

    class Meta:
        model = ProductTypeSelectorValue
        fields = ['search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            Q(value__contains=value) | Q(digikala_id=value)
        )


class VariantFilter(filters.FilterSet):
    product_title = filters.CharFilter(field_name='product', lookup_expr='title__contains')
    search = filters.CharFilter(method='search_in_fields')

    class Meta:
        model = ProductVariant
        fields = ['product', 'search']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            Q(product__title__contains=value) | Q(dkpc=value)
        )
