from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from shop.models import ProductAttribute
from shop.serializers import ProductAttributeReadWriteSerializer
from shop.api.filters import ProductAttributeFilter
from utils.drf.mixins import GetByIdList
from utils.drf.permissions import IsAdmin


__all__ = [
    'ProductAttributeViewSet',
]


class ProductAttributeViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              GenericViewSet,
                              GetByIdList):
    queryset = ProductAttribute.objects.all().order_by('id')
    serializer_class = ProductAttributeReadWriteSerializer
    filterset_class = ProductAttributeFilter
    permission_classes = [IsAdmin]
