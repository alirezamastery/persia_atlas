from django.db.models import Q
from django_filters import rest_framework as filters

from ..models import Product, ActualProduct, ProductVariant


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = Product
        fields = ['title']


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


class ActualProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = ActualProduct
        fields = ['title']
