from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

from shop.api.filters import ProductVariantFilter
from shop.models import *
from shop.serializers import *
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'ProductVariantViewSet',
]


class ProductVariantViewSet(ModelViewSet):
    queryset = ProductVariant.objects \
        .select_related('product') \
        .select_related('selector_value__type') \
        .all() \
        .order_by('id')
    filterset_class = ProductVariantFilter
    permission_classes = [IsAdmin | ReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductVariantReadSerializer
        return ProductVariantWriteSerializer
