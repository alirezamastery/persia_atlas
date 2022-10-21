from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from products.models import *
from products.serializers import *
from products.api.filters import *


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductReadSerializer
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductReadSerializer
        return ProductWriteSerializer


class ProductTypeViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = ProductType.objects.all().order_by('-id')
    filterset_class = ProductTypeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductTypeReadSerializer
        return ProductTypeWriteSerializer


__all__ = [
    'ProductViewSet',
    'ProductTypeViewSet',
]
