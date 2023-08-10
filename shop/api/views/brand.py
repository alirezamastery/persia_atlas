from rest_framework.viewsets import ModelViewSet

from shop.models import Brand
from shop.serializers import BrandReadWriteSerializer
from shop.api.filters import BrandFilter
from utils.drf.permissions import IsAdmin


__all__ = [
    'BrandViewSet',
]


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandReadWriteSerializer
    permission_classes = [IsAdmin]
    filterset_class = BrandFilter
