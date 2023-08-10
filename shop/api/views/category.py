from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from shop.models import *
from shop.serializers.category import *
from shop.api.filters import CategoryFilter
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'CategoryViewSetPublic',
    'CategoryViewsetAdmin',
]


class CategoryViewSetPublic(ReadOnlyModelViewSet):
    queryset = Category.objects \
        .select_related('selector_type') \
        .all() \
        .order_by('id')
    permission_classes = [ReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductCategoryListSerializer
        return ProductCategoryDetailSerializer

    @action(detail=False, methods=['GET'], url_path='get-tree')
    def get_tree(self, request):
        tree_structure = Category.dump_bulk_custom()
        return Response({'tree': tree_structure})


class CategoryViewsetAdmin(ModelViewSet):
    queryset = Category.objects \
        .select_related('selector_type') \
        .all() \
        .order_by('id')
    filterset_class = CategoryFilter
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
