from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from products.models import *
from products.serializers import *
from products.api.filters import *
from products.tasks import toggle_variants_status
from persia_atlas.drf import OptionalPagination


class ProductVariantViewSet(OptionalPagination,
                            mixins.CreateModelMixin,
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

    @action(detail=False, methods=['get'], url_path='get-by-dkpc-list')
    def get_by_dkpc_list(self, request):
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

    @action(detail=False, methods=['POST'], url_path='toggle-status')
    def toggle_status(self, request):
        serializer = ToggleVariantStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = toggle_variants_status.delay(
            data['actual_product_id'],
            data['selector_ids'],
            data['is_active'],
        )
        return Response({'task_id': task.id})


__all__ = [
    'ProductVariantViewSet'
]
