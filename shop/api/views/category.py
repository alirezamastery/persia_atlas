from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from shop.models import *
from shop.serializers import *
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
    serializer_class = ProductCategoryReadSerializer


class CategoryAdminViewset(ModelViewSet):
    queryset = ProductCategory.objects \
        .select_related('selector_type') \
        .all() \
        .order_by('id')
    filterset_class = ProductCategoryFilter
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductCategoryReadSerializer
        return ProductCategoryWriteSerializer

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        if response.data['next'] is None:
            response.data['items'].insert(0, {
                'id':    0,
                'title': '-- سرشاخه --'
            })
        return response

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, context={'with_details': True})
        return Response(serializer.data)
