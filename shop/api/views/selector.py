from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import SelectorType
from shop.serializers import VariantSelectorTypeReadSerializer


__all__ = [
    'VariantSelectorTypeViewSet',
]


class VariantSelectorTypeViewSet(ReadOnlyModelViewSet):
    queryset = SelectorType.objects.all().order_by('id')
    serializer_class = VariantSelectorTypeReadSerializer
