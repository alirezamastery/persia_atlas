from django.core.cache import cache
from django.conf import settings

from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from celery.result import AsyncResult

from products.models import *
from products.serializers import *
from products.api.filters import *
from scripts.json_db import JsonDB
from ...tasks import scrape_invoice_page, just_sleep, just_sleep_and_fail
from utils.logging import logger, plogger


class NoDeleteModelViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    pass


class BrandViewSet(NoDeleteModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filterset_class = BrandFilter


class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = None


class ActualProductByBrandView(APIView):

    def get(self, request, brand_id):
        qs = ActualProduct.objects.filter(brand__id=brand_id)
        serializer = BrandSerializer(qs, many=True)
        return Response(serializer.data)


class ActualProductViewSet(ModelViewSet):
    queryset = ActualProduct.objects.all().order_by('-id')
    serializer_class = ActualProductSerializer
    filterset_class = ActualProductFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActualProductSerializer
        return ActualProductWriteSerializer

    @action(detail=True, methods=['get'])
    def related_selectors(self, request, pk=None):
        actual_product = self.get_object()
        variants = actual_product.variants.all()
        selector_ids = []
        for var in variants:
            selector_ids.append(var.selector.id)
        selector_ids = set(selector_ids)
        selector_values = VariantSelector.objects.filter(id__in=selector_ids)
        serializer = VariantSelectorSerializer(selector_values, many=True)
        return Response(serializer.data)


class ProductViewSet(NoDeleteModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductReadSerializer
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductReadSerializer
        return ProductWriteSerializer


class ProductTypeViewSet(NoDeleteModelViewSet):
    queryset = ProductType.objects.all().order_by('-id')
    filterset_class = ProductTypeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductTypeReadSerializer
        return ProductTypeWriteSerializer


class VariantSelectorTypeViewSet(NoDeleteModelViewSet):
    queryset = VariantSelectorType.objects.all().order_by('-id')
    serializer_class = VariantSelectorTypeSerializer
    filterset_class = VariantSelectorTypeFilter

    @action(detail=False, methods=['get'])
    def get_by_list(self, request):
        ids = request.query_params.getlist('ids[]')
        qs = self.queryset.filter(pk__in=ids)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)


class VariantSelectorViewSet(ReadOnlyModelViewSet):
    queryset = VariantSelector.objects.all().order_by('digikala_id')
    serializer_class = VariantSelectorSerializer
    filterset_class = VariantSelectorFilter

    @action(detail=False, methods=['get'])
    def get_by_list(self, request):
        ids = request.query_params.getlist('ids[]')
        qs = self.queryset.filter(pk__in=ids)
        serializer = self.get_serializer_class()(qs, many=True)
        return Response(serializer.data)


class ProductVariantViewSet(NoDeleteModelViewSet):
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


class DigiLoginCredentialsView(APIView):

    def get(self, request):
        db = JsonDB()
        response = {
            JsonDB.keys.DIGI_USERNAME: db.get(JsonDB.keys.DIGI_USERNAME),
            JsonDB.keys.DIGI_PASSWORD: db.get(JsonDB.keys.DIGI_PASSWORD),
        }
        return Response(response)

    def post(self, request):
        db = JsonDB()
        username = request.data.get(JsonDB.keys.DIGI_USERNAME, db.get(JsonDB.keys.DIGI_USERNAME))
        password = request.data.get(JsonDB.keys.DIGI_PASSWORD, db.get(JsonDB.keys.DIGI_PASSWORD))
        db.set(JsonDB.keys.DIGI_USERNAME, username)
        db.set(JsonDB.keys.DIGI_PASSWORD, password)
        response = {
            JsonDB.keys.DIGI_USERNAME: username,
            JsonDB.keys.DIGI_PASSWORD: password,
        }
        return Response(response, status=status.HTTP_201_CREATED)


class ScrapeInvoiceView(APIView):

    def post(self, request):
        serializer = ScrapeInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        row_number = serializer.validated_data['row_number']
        task = scrape_invoice_page.delay(row_number)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class TestCelerySuccessTask(APIView):

    def post(self, request):
        task = just_sleep.delay()
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class TestCeleryFailTask(APIView):

    def post(self, request):
        task = just_sleep_and_fail.delay()
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class CeleryTaskStateView(APIView):

    def get(self, request, task_id):
        task = AsyncResult(task_id)

        if task.state == 'FAILURE' or task.state == 'PENDING':
            response = {
                'task_id':     task_id,
                'state':       task.state,
                'progression': None,
                'info':        str(task.info)
            }
            return Response(response, status=200)
        response = {
            'task_id': task_id,
            'state':   task.state,
            'info':    None
        }
        return Response(response, status=200)


class RobotVariantsFilterView(APIView):

    def get(self, request):
        actual_product_id = request.query_params.get('actual_product_id')
        selector_id = request.query_params.get('selector_id')
        variants = ProductVariant.objects.filter(
            selector_id=selector_id,
            actual_product_id=actual_product_id
        ).order_by('id')
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)


class RobotStatusView(APIView):

    def get(self, request):
        if cache.get(settings.CACHE_KEY_STOP_ROBOT) == 'true':
            running = False
        else:
            running = True
        return Response({'running': running})

    def post(self, request):
        serializer = StopRobotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stop = serializer.data.get('stop')
        logger(f'ROBOT STOP SIGNAL: {stop}')
        if stop is True:
            cache.set(settings.CACHE_KEY_STOP_ROBOT, 'true', timeout=None)
        else:
            cache.set(settings.CACHE_KEY_STOP_ROBOT, 'false', timeout=None)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


__all__ = [
    'BrandViewSet',
    'BrandListView',
    'ActualProductByBrandView',
    'ActualProductViewSet',
    'ProductViewSet',
    'ProductTypeViewSet',
    'VariantSelectorTypeViewSet',
    'VariantSelectorViewSet',
    'ProductVariantViewSet',
    'DigiLoginCredentialsView',
    'ScrapeInvoiceView',
    'TestCelerySuccessTask',
    'TestCeleryFailTask',
    'CeleryTaskStateView',
    'RobotVariantsFilterView',
    'RobotStatusView',
]
