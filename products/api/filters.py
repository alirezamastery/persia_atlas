from django_filters import rest_framework as filters

from ..models import Product, ActualProduct, ProductVariant


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = Product
        fields = ['title']


class VariantFilter(filters.FilterSet):
    product_title = filters.CharFilter(field_name='product', lookup_expr='title__contains')

    class Meta:
        model = ProductVariant
        fields = ['product']


class ActualProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = ActualProduct
        fields = ['title']
