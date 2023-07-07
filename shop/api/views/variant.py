from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

from ..filters import VariantSelectorTypeFilter
from shop.models import *
from shop.serializers import *
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'ProductVariantViewSet',
]


class ProductVariantViewSet(ModelViewSet):
    queryset = ProductVariant.objects.all()
    permission_classes = [IsAdmin | ReadOnly]
    filterset_class = VariantSelectorTypeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductVariantReadSerializer
        return ProductVariantWriteSerializer
