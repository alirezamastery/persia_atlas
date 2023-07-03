from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from shop.models import *
from shop.serializers import *
from shop.queries import get_product_with_attrs
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'ProductViewSet',
]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects \
        .select_related('brand') \
        .select_related('category') \
        .all() \
        .order_by('id')
    permission_classes = [IsAdmin | ReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action == 'retrieve' or self.action == 'get_with_details':
            return ProductDetailSerializer
        return ProductWriteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'get_with_details':
            context['get_variants'] = True
        return context

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_product_with_attrs(pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='with-details')
    def get_with_details(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_product_with_attrs(pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)
