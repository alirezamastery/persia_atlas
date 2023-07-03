from rest_framework.viewsets import ModelViewSet

from shop.models import Brand
from shop.serializers import BrandSerializer
from utils.drf.permissions import IsAdmin


__all__ = [
    'BrandViewSet',
]


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer
    permission_classes = [IsAdmin]
