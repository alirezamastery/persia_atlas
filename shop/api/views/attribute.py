from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from shop.models import Attribute
from shop.serializers import AttributeReadWriteSerializer
from shop.api.filters import AttributeFilter
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
    queryset = Attribute.objects.all().order_by('id')
    serializer_class = AttributeReadWriteSerializer
    filterset_class = AttributeFilter
    permission_classes = [IsAdmin]
