from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.serializers.category import *
from shop.api.filters import ProductCategoryFilter
from utils.drf.permissions import IsAdmin


__all__ = [
    'CategoryViewSet',
    'CategoryAdminViewset',
]


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = ProductCategory.objects \
        .select_related('selector_type') \
        .all() \
        .order_by('id')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductCategoryListSerializer
        return ProductCategoryDetailSerializer


class CategoryAdminViewset(ModelViewSet):
    queryset = ProductCategory.objects \
        .select_related('selector_type') \
        .all() \
        .order_by('id')
    filterset_class = ProductCategoryFilter
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductCategoryListSerializer
        if self.action == 'retrieve' or self.request.method in SAFE_METHODS:
            return ProductCategoryDetailSerializer
        return ProductCategoryWriteSerializer

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        if response.data['next'] is None:
            response.data['items'].insert(0, {
                'id':    0,
                'title': '-- سرشاخه --'
            })
        return response
