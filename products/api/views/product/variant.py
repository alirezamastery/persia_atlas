import time

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from products.models import *
from products.serializers import *
from products.api.filters import *
from utils.drf.pagination import OptionalPagination
from utils.digi import variant_detail_request


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
        # task = toggle_variants_status.delay(
        #     data['actual_product_id'],
        #     data['selector_ids'],
        #     data['is_active'],
        # )
        actual_product_id = data['actual_product_id']
        selector_ids = data['selector_ids']
        is_active = data['is_active']

        dkpc_list = ProductVariant.objects \
            .filter(actual_product_id=actual_product_id, selector_id__in=selector_ids) \
            .values_list('dkpc', flat=True)

        digi_errors = []
        handled_variants = []
        if is_active is True:
            for dkpc in dkpc_list:
                try:
                    variant_detail_request(dkpc, method='PUT', payload={'seller_stock': 3})
                except APIException as e:
                    digi_errors.append(e.get_full_details())
                time.sleep(0.2)

        for dkpc in dkpc_list:
            try:
                variant_detail_request(dkpc, method='PUT', payload={'is_active': is_active})
                handled_variants.append(dkpc)
            except APIException as e:
                digi_errors.append(e.get_full_details())
            time.sleep(0.2)

        variants = ProductVariant.objects.filter(dkpc__in=handled_variants)
        for variant in variants:
            variant.is_active = is_active
        ProductVariant.objects.bulk_update(variants, fields=['is_active'])

        return Response({'has_error': len(digi_errors) > 0, 'errors': digi_errors})


__all__ = [
    'ProductVariantViewSet'
]
