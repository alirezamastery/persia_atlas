from rest_framework.generics import ListAPIView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from products.models import *
from products.serializers import *
from products.api.filters import *


class BrandViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filterset_class = BrandFilter


class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = None


__all__ = [
    'BrandViewSet',
    'BrandListView'
]
