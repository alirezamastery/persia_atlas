import json

import requests
from django.conf import settings
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status

from utils.logging import logger, plogger
from ..models import Product, ProductVariant, ProductType, ProductTypeSelector, ProductTypeSelectorValue
from ..serializers import (ProductSerializer, ProductVariantSerializer, ProductTypeSerializer,
                           ProductTypeSelectorSerializer, ProductTypeSelectorValueSerializer,
                           VariantSerializerDigikalaContext)


class ProductVariantsViewSet(RetrieveModelMixin,
                             UpdateModelMixin,
                             ListModelMixin,
                             GenericViewSet):
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        print(res.data)
        for d in res.data:
            print(d)
        return res


class ProductVariantsListView(APIView):

    def get(self, request):
        session = requests.Session()
        response = session.post(settings.DIGIKALA_LOGIN_URL,
                                data=settings.DIGIKALA_LOGIN_CREDENTIALS,
                                timeout=30)
        print(response)
        logger(response, color='yellow')
        logger(f'{response.url = }', color='yellow')
        if response.url == settings.DIGIKALA_LOGIN_URL:
            raise Exception('could not login')

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
        # plogger(digi_items)

        variants = ProductVariant.objects.all()
        serialized = []
        for variant in variants:
            # print(variant.dkpc)
            for item in digi_items:
                print(item)
                if variant.dkpc == str(item['product_variant_id']):
                    print(variant.dkpc)
                    serialized.append(
                        VariantSerializerDigikalaContext(variant, context={'digi_data': item}).data
                    )
                    break
        plogger(serialized)
        return Response(serialized, status=status.HTTP_200_OK)
