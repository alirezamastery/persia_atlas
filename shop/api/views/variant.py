from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action

from ..filters import VariantSelectorTypeFilter
from shop.models import *
from shop.serializers import *
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'ProductVariantViewSet',
    'VariantSelectorTypeViewSet',
]


class ProductVariantViewSet(ModelViewSet):
    queryset = ProductVariant.objects.all()
    permission_classes = [IsAdmin | ReadOnly]
    filterset_class = VariantSelectorTypeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductVariantReadSerializer
        return ProductVariantWriteSerializer


class VariantSelectorTypeViewSet(ReadOnlyModelViewSet):
    queryset = VariantSelectorType.objects.all().order_by('id')
    serializer_class = VariantSelectorTypeSerializer
