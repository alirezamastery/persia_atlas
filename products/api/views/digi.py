import time

import pandas as pd
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.logging import logger, plogger
from utils.digi import get_variant_search_url
from products.models import *
from products.serializers import *
from products.tasks import update_brand_status
from persia_atlas.digi import digi_session


class ActualProductDigikalaDataView(APIView):

    def get(self, request, pk):
        product = ActualProduct.objects.get(pk=pk)
        dkpc_list = product.variants.all().values_list('dkpc', flat=True)
        logger(f'{dkpc_list = }')

        digi_items = {}
        for dkpc in dkpc_list:
            url = get_variant_search_url(dkpc)
            res = digi_session.get(url)
            if not res['status']:
                return Response({'error': 'دیجیکالا رید'}, status=status.HTTP_404_NOT_FOUND)
            logger(f'{dkpc:*^50}')
            plogger(res)
            if len(res['data']['items']) == 0:
                return Response({'error': f'no variant with dkpc: {dkpc} in digikala site'},
                                status.HTTP_404_NOT_FOUND)
            digi_items[dkpc] = res['data']['items'][0]
            time.sleep(2)

        serialized = []
        for dkpc, data in digi_items.items():
            variant = ProductVariant.objects.get(dkpc=dkpc)
            serialized.append(
                VariantSerializerDigikalaContext(variant, context={'digi_data': data}).data
            )

        response = {
            'product':  ActualProductSerializer(product).data,
            'variants': serialized
        }

        return Response(response, status=status.HTTP_200_OK)


class VariantDigiDataView(APIView):

    def get(self, request, pk):
        variant = get_object_or_404(ProductVariant, pk=pk)
        dkpc = variant.dkpc
        url = get_variant_search_url(dkpc)
        res = digi_session.get(url)
        if not res['status']:
            return Response({'error': 'دیجیکالا رید'}, status=status.HTTP_400_BAD_REQUEST)
        logger(f'{dkpc:*^50}')
        plogger(res)
        if len(res['data']['items']) == 0:
            return Response({'error': f'no variant with dkpc: {dkpc} in digikala site'},
                            status.HTTP_404_NOT_FOUND)
        data = res['data']['items'][0]
        serializer = VariantSerializerDigikalaContext(variant, context={'digi_data': data})
        return Response(serializer.data)


class VariantDigiDataDKPCView(APIView):

    def get(self, request, dkpc):
        variant = get_object_or_404(ProductVariant, dkpc=dkpc)
        url = get_variant_search_url(dkpc)
        res = digi_session.get(url)
        if not res['status']:
            return Response({'error': 'دیجیکالا رید'}, status=status.HTTP_400_BAD_REQUEST)
        if len(res['data']['items']) == 0:
            return Response({'error': f'no variant with dkpc: {dkpc} in digikala site'},
                            status.HTTP_404_NOT_FOUND)
        data = res['data']['items'][0]
        serializer = VariantSerializerDigikalaContext(variant, context={'digi_data': data})
        return Response(serializer.data)


class UpdateVariantDigiDataView(APIView):

    def post(self, request):
        serializer = UpdateVariantDigiDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        payload = {
            'id':                        data['dkpc'],
            'lead_time':                 '1',
            'price_sale':                data['price'],
            'marketplace_seller_stock':  data['our_stock'],
            'maximum_per_order':         '5',
            'oldSellerStock':            '1',
            'selling_chanel':            '',
            'is_buy_box_suggestion':     '0',
            'shipping_type':             'digikala',
            'seller_shipping_lead_time': '2',
        }
        digikala_res = digi_session.post(settings.DIGIKALA_URLS['update_variant_data'], payload)
        plogger(digikala_res)
        if digikala_res['status']:
            return Response(digikala_res['data'], status.HTTP_200_OK)

        return Response(digikala_res['data'], status.HTTP_400_BAD_REQUEST)


class UpdateVariantStatusView(APIView):

    def post(self, request):
        serializer = UpdateVariantStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        payload = {
            'id':     data['dkpc'],
            'active': data['is_active']
        }
        digikala_res = digi_session.post(settings.DIGIKALA_URLS['update_variant_status'], payload)
        plogger(digikala_res)
        if digikala_res['status']:
            variant = ProductVariant.objects.get(dkpc=data['dkpc'])
            variant.is_active = data['is_active']
            variant.save()
            return Response(digikala_res['data'], status.HTTP_202_ACCEPTED)

        return Response(digikala_res['data'], status.HTTP_408_REQUEST_TIMEOUT)


class UpdateBrandVariantsStatusView(APIView):

    def post(self, request):
        serializer = UpdateBrandStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        task = update_brand_status.delay(data['id'], data['is_active'])
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class UpdatePriceMinView(APIView):

    def post(self, request):
        serializer = UpdateVariantPriceMinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        variant = ProductVariant.objects.get(dkpc=data['dkpc'])
        variant.price_min = data['price_min']
        variant.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)


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
        url = 'https://seller.digikala.com/ajax/variants/search/?sortColumn=&sortOrder=desc&page=1&items=100&search[active]=2'
        res = digi_session.get(url)
        return Response(res['data'])


__all__ = [
    'ActualProductDigikalaDataView',
    'UpdateVariantDigiDataView',
    'UpdateVariantStatusView',
    'UpdateBrandVariantsStatusView',
    'UpdatePriceMinView',
    'FileDownloadTest',
    'VariantDigiDataView',
    'InactiveVariantsView',
    'VariantDigiDataDKPCView'
]
