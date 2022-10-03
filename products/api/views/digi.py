import pandas as pd
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.digi import *
from products.models import *
from products.serializers import *
from products.tasks import update_brand_status


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
        digi_response = variant_detail_request(variant.dkpc, method='PUT', payload=serializer.validated_data)
        return Response(digi_response)


class UpdateBrandVariantsStatusView(APIView):

    def post(self, request):
        serializer = UpdateBrandStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        task = update_brand_status.delay(data['id'], data['is_active'])
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class FileDownloadTest(APIView):
    file_name = 'quantity.xlsx'

    def get(self, request):
        dfs = []
        for _ in range(2):
            df = self.calculate_quantities()
            dfs.append(df)

        overview = pd.concat(dfs)
        overview.set_index(['date', 'name'], inplace=True)

        file_path = f'{settings.MEDIA_DIR_NAME}/invoice/{self.file_name}'
        with open(file_path, 'wb+') as file:
            overview.to_excel(file, sheet_name='products')
            file_url = file_path
        return Response({'path': file_url}, status.HTTP_200_OK)

    @staticmethod
    def calculate_quantities():
        names = [x for x in range(10)]
        quantities = [x for x in range(10)]
        df = pd.DataFrame({'name': names, 'quantity': quantities})
        df['date'] = 'test date'
        return df


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
    'UpdateVariantDigiDataView',
    'UpdateBrandVariantsStatusView',
    'FileDownloadTest',
    'VariantDigiDataView',
    'InactiveVariantsView',
    'VariantDigiDataDKPCView'
]
