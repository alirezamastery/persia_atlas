from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from utils.drf.mixins import GetByIdList
from ..filters import ProductAttributeFilter
from shop.models import ProductAttribute
from shop.serializers import ProductAttributeSerializer
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
    serializer_class = ProductAttributeSerializer
    filterset_class = ProductAttributeFilter
    permission_classes = [IsAdmin]
