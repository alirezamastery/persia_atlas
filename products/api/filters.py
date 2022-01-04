from django_filters import rest_framework as filters

from ..models import Product, ActualProduct


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = Product
        fields = ['title']


class ActualProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = ActualProduct
        fields = ['title']
