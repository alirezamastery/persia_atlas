import json
from pprint import pprint

import requests
from django.conf import settings
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.logging import logger, plogger
from ..models import (ProductVariant, ActualProduct)
from ..serializers import (UpdateVariantPriceMinSerializer, UpdateVariantDigiDataSerializer,
                           UpdateVariantStatusSerializer, VariantSerializerDigikalaContext,
                           ActualProductSerializer, DKPCListSerializer)


def digikala_login_session():
    session = requests.Session()
    while True:
        response = session.post(settings.DIGIKALA_LOGIN_URL,
                                data=settings.DIGIKALA_LOGIN_CREDENTIALS,
                                timeout=30)
        logger(response, color='yellow')
        logger(f'{response.url = }', color='yellow')
        if response.url == settings.DIGIKALA_LOGIN_URL:
            continue
        return session


def get_variant_search_url(dkpc):
    return f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&' \
           f'sortOrder=desc&page=1&items=10&search[type]=product_variant_id&search[value]={dkpc}&'


class ProductVariantsListView(APIView):

    def get(self, request):
        session = digikala_login_session()

        digi_items = []
        while True:
            counter = 1
            url = f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&sortOrder=desc&page={counter}&items=200&'
            digikala_res = session.get(url, timeout=30)
            res = digikala_res.json()
            if not res['status']:
                return Response({'error': 'دیجیکالا رید'}, status=status.HTTP_404_NOT_FOUND)
            digi_items += (res['data']['items'])
            if counter <= res['data']['pager']['totalPage']:
                break
            counter += 1

        variants = ProductVariant.objects.all()
        serialized = []
        for variant in variants:
            for item in digi_items:
                if variant.dkpc == str(item['product_variant_id']):
                    serialized.append(
                        VariantSerializerDigikalaContext(variant, context={'digi_data': item}).data
                    )
                    break
        plogger(serialized)
        return Response(serialized, status=status.HTTP_200_OK)


class ActualProductViewSet(ReadOnlyModelViewSet):
    queryset = ActualProduct.objects.all()
    serializer_class = ActualProductSerializer


class ProductVariantDigikalaDataView(APIView):

    def post(self, request):
        dkpc_list = request.data.get('dkpc_list')
        print(request.data)
        serializer = DKPCListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        print(serializer.data)
        session = digikala_login_session()
        digi_items = {}
        for dkpc in dkpc_list:
            url = f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&' \
                  f'sortOrder=desc&page=1&items=10&search[type]=product_variant_id&search[value]={dkpc}&'
            digikala_res = session.get(url, timeout=30)
            res = digikala_res.json()
            if not res['status']:
                return Response({'error': 'دیجیکالا رید'}, status=status.HTTP_404_NOT_FOUND)
            digi_items[dkpc] = res['data']['items'][0]

        serialized = []
        for dkpc, data in digi_items.items():
            variant = ProductVariant.objects.get(dkpc=dkpc)
            serialized.append(
                VariantSerializerDigikalaContext(variant, context={'digi_data': data}).data
            )

        return Response(serialized, status=status.HTTP_200_OK)


class ActualProductDigikalaDataView(APIView):

    def get(self, request, pk):
        product = ActualProduct.objects.get(pk=pk)
        dkpc_list = product.variants.all().values_list('dkpc', flat=True)

        session = digikala_login_session()
        digi_items = {}
        for dkpc in dkpc_list:
            url = get_variant_search_url(dkpc)
            digikala_res = session.get(url, timeout=30)
            res = digikala_res.json()
            if not res['status']:
                return Response({'error': 'دیجیکالا رید'}, status=status.HTTP_404_NOT_FOUND)
            digi_items[dkpc] = res['data']['items'][0]
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


class UpdateVariantDigiDataView(APIView):

    def post(self, request):
        serializer = UpdateVariantDigiDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        session = digikala_login_session()
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
        digikala_res = session.post(settings.DIGIKALA_URLS['update_variant_data'],
                                    data=payload)
        digikala_res = digikala_res.json()
        plogger(digikala_res)
        if digikala_res['status']:
            return Response(digikala_res['data'], status.HTTP_200_OK)
        return Response(digikala_res['data'], status.HTTP_400_BAD_REQUEST)


class UpdateVariantStatusView(APIView):

    def post(self, request):
        serializer = UpdateVariantStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        session = digikala_login_session()
        payload = {
            'id':     data['dkpc'],
            'active': data['is_active']
        }
        digikala_res = session.post(settings.DIGIKALA_URLS['update_variant_status'],
                                    data=payload)
        digikala_res = digikala_res.json()
        plogger(digikala_res)
        if digikala_res['status']:
            variant = ProductVariant.objects.get(dkpc=data['dkpc'])
            variant.is_active = data['is_active']
            variant.save()
            return Response(digikala_res['data'], status.HTTP_202_ACCEPTED)
        return Response(digikala_res['data'], status.HTTP_400_BAD_REQUEST)


class UpdatePriceMinView(APIView):

    def post(self, request):
        serializer = UpdateVariantPriceMinSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        variant = ProductVariant.objects.get(dkpc=data['dkpc'])
        variant.price_min = data['price_min']
        variant.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
