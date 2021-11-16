import json
import time
import pickle
from pathlib import Path
from pprint import pprint

import pandas as pd
import requests
from django.conf import settings
from django.http import FileResponse
from django.core.files.storage import default_storage
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import BaseRenderer
from django_filters import rest_framework as filters

from utils.logging import logger, plogger
from utils.digi import get_variant_search_url
from ..models import (ProductVariant, ActualProduct, Brand, Invoice, InvoiceItem)
from ..serializers import (
    UpdateVariantPriceMinSerializer, UpdateVariantDigiDataSerializer,
    UpdateVariantStatusSerializer, VariantSerializerDigikalaContext,
    ActualProductSerializer, DKPCListSerializer, BrandSerializer,
    ProductVariantSerializer, ProductVariantUpdateSerializer,
    InvoiceSerializer, InvoiceItemSerializer
)


class DigikalaSession:
    COOKIE_FILE = 'session_cookies'
    TIMEOUT = 10
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}

    def __init__(self):
        self.session = requests.Session()
        cookie_file = Path(f'./{self.COOKIE_FILE}')
        if cookie_file.is_file():
            logger('loading cookies', color='yellow')
            with open('session_cookies', 'rb') as f:
                self.session.cookies.update(pickle.load(f))
        else:
            self.login()

    def login(self):
        logger('logging in', color='yellow')
        response = self.session.post(settings.DIGIKALA_LOGIN_URL,
                                     data=settings.DIGIKALA_LOGIN_CREDENTIALS,
                                     timeout=10,
                                     headers=self.HEADERS)
        if response.url == settings.DIGIKALA_URLS['login']:
            raise Exception('could not login to digikala')
        logger('logged in', color='green')
        with open(f'./{self.COOKIE_FILE}', 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def post(self, url, payload):
        response = self.session.post(url,
                                     data=payload,
                                     timeout=self.TIMEOUT,
                                     headers=self.HEADERS)
        if 'account/login' in response.url:
            self.login()
            return self.post(url, payload)
        return response.json()

    def get(self, url):
        response = self.session.get(url,
                                    timeout=self.TIMEOUT,
                                    headers=self.HEADERS)
        if 'account/login' in response.url:
            self.login()
            return self.get(url)
        logger(response.url)
        return response.json()


digi_session = DigikalaSession()


class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ActualProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = ActualProduct
        fields = ['title']


class ActualProductViewSet(ReadOnlyModelViewSet):
    queryset = ActualProduct.objects.all()
    serializer_class = ActualProductSerializer
    filterset_class = ActualProductFilter


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
            time.sleep(0.5)

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


class UpdatePriceMinView(APIView):

    def post(self, request):
        serializer = UpdateVariantPriceMinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        variant = ProductVariant.objects.get(dkpc=data['dkpc'])
        variant.price_min = data['price_min']
        variant.save()
        return Response(serializer.data, status.HTTP_202_ACCEPTED)


class ProductVariantViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = ProductVariant.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ProductVariantUpdateSerializer
        return ProductVariantSerializer


class InvoiceViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceItemViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

    @action(detail=False, methods=['post'])
    def bulk_insert(self, request):
        serializer = InvoiceItemSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        for item in serializer.data:
            invoice = Invoice.objects.get(pk=item.pop('invoice'))
            InvoiceItem.objects.create(**item, invoice=invoice)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PassthroughRenderer(BaseRenderer):
    """
    Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class InvoiceExcelView(APIView):
    file_name = 'quantity.xlsx'

    def get(self, request):
        invoices = Invoice.objects.all()
        dfs = []
        for invoice in invoices:
            df = self.calculate_quantities(invoice)
            dfs.append(df)
        overview = pd.concat(dfs)
        overview.set_index(['date', 'name'], inplace=True)

        file_path = f'{settings.MEDIA_DIR_NAME}/invoice/{self.file_name}'
        with open(file_path, 'wb+') as file:
            overview.to_excel(file, sheet_name='products')

        return Response({'path': file_path}, status.HTTP_200_OK)

    @staticmethod
    def calculate_quantities(invoice_obj: Invoice):
        items = InvoiceItem.objects.filter(invoice=invoice_obj)
        dkp_data = {}
        serials = []

        for item in items:
            if item.serial in serials:
                continue
            variant = ProductVariant.objects.select_related('product').get(dkpc=item.dkpc)
            dkp = variant.product.dkp
            if dkp in dkp_data:
                dkp_data[dkp]['count'] += 1
            else:
                dkp_data[dkp] = {
                    'count': 1,
                    'name':  variant.product.title
                }

            serials.append(item.serial)
        pprint(dkp_data)
        names = []
        quantities = []
        for q in dkp_data.values():
            names.append(q['name'])
            quantities.append(q['count'])
        df = pd.DataFrame({'name': names, 'quantity': quantities})
        df['date'] = f'{invoice_obj.start_date} - {invoice_obj.end_date}'
        return df


class FileDownloadTest(APIView):
    file_name = 'quantity.xlsx'

    def get(self, request):
        dfs = []
        for _ in range(2):
            df = self.calculate_quantities()
            dfs.append(df)

        overview = pd.concat(dfs)
        overview.set_index(['date', 'name'], inplace=True)

        # with open(self.file_name, 'wb+') as file:
        #     overview.to_excel(file, sheet_name='products')
        #     file_path = f'invoice/{self.file_name}'
        #     saved_file = default_storage.save(file_path, file)
        #     file_url = default_storage.url(saved_file)
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
