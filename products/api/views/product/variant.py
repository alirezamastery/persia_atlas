from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from products.models import *
from products.serializers import *
from products.api.filters import *


class ProductVariantViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = ProductVariant.objects.all().order_by('-id')
    filterset_class = VariantFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductVariantSerializer
        return ProductVariantWriteSerializer

    @action(detail=False, methods=['get'])
    def get_by_list(self, request):
        dkpc_list = request.query_params.getlist('dkpc[]')
        qs = self.queryset.filter(dkpc__in=dkpc_list)
        serializer = self.get_serializer_class()(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='bulk-create')
    def bulk_create(self, request):
        serializer = ProductVariantBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'info': 'ok'})


__all__ = [
    'ProductVariantViewSet'
]
