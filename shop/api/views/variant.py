from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework import mixins

from shop.api.filters import VariantFilter
from shop.models import Variant
from shop.serializers import VariantReadSerializer, VariantUpdateSerializer
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'ProductVariantViewSet',
]


class ProductVariantViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Variant.objects \
        .select_related('product') \
        .select_related('selector_value__type') \
        .all() \
        .order_by('id')
    filterset_class = VariantFilter
    permission_classes = [IsAdmin | ReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return VariantReadSerializer
        return VariantUpdateSerializer
