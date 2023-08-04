from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from shop.models import Product
from shop.serializers import *
from shop.api.filters import ProductFilter
from shop.queries import get_product_with_attrs
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'ProductViewSet',
]


class ProductViewSet(ModelViewSet):
    # queryset = Product.objects \
    #     .select_related('brand') \
    #     .select_related('category') \
    #     .prefetch_related('variants__selector_value__type') \
    #     .all() \
    #     .order_by('id')
    filterset_class = ProductFilter
    permission_classes = [IsAdmin | ReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductWriteSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Product.objects \
                .select_related('brand') \
                .select_related('category') \
                .prefetch_related('variants__selector_value__type') \
                .all() \
                .order_by('id')
        return Product.objects \
            .select_related('brand') \
            .select_related('category') \
            .prefetch_related('variants__selector_value__type') \
            .prefetch_related('attribute_values') \
            .all() \
            .order_by('id')

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_product_with_attrs(pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='add-variants')
    def add_variants(self, request, *args, **kwargs):
        serializer = ProductVariantCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
