from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.digi import *
from products.models import *
from products.serializers import *


class VariantDigiDataView(APIView):

    def get(self, request, pk):
        variant = get_object_or_404(ProductVariant, pk=pk)
        data = variant_detail_request(variant.dkpc)
        serializer = VariantSerializerDigikalaContext(variant, context={'digi_data': data})
        return Response(serializer.data)


class VariantDigiDataDKPCView(APIView):

    def get(self, request, dkpc):
        variant = get_object_or_404(ProductVariant, dkpc=dkpc)
        data = variant_detail_request(variant.dkpc, method='GET')
        serializer = VariantSerializerDigikalaContext(variant, context={'digi_data': data})
        return Response(serializer.data)


class UpdateVariantDigiDataView(APIView):

    def post(self, request, dkpc):
        variant = get_object_or_404(ProductVariant, dkpc=dkpc)
        serializer = UpdateVariantDigiDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        digi_response = variant_detail_request(
            variant.dkpc,
            method='PUT',
            payload=serializer.validated_data
        )
        return Response(digi_response)


class InactiveVariantsView(APIView):

    def get(self, request):
        query_params = {'search[is_active]': '0'}
        res = get_variant_list(query_params)
        total_count = res['pager']['total_rows']
        items = res['items']

        total_pages = res['pager']['page']
        page = res['pager']['total_page']
        if total_pages > 1:
            while page < total_pages:
                page += 1
                query_params['page'] = page
                res = get_variant_list(query_params)
                items.extend(res['items'])

        response = {
            'total_count': total_count,
            'items':       items
        }
        return Response(response)


__all__ = [
    'VariantDigiDataView',
    'VariantDigiDataDKPCView',
    'UpdateVariantDigiDataView',
    'InactiveVariantsView',
]
