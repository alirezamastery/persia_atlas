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


__all__ = [
    'BrandViewSet', 'ActualProductViewSet', 'ProductViewSet', 'ProductTypeViewSet', 'ProductTypeSelectorViewSet',
    'ProductTypeSelectorValueViewSet', 'ProductVariantViewSet', 'InvoiceViewSet', 'InvoiceItemViewSet',
    'DigiLoginCredentialsView', 'ScrapeInvoiceView', 'CeleryTaskStateView'
]


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


__all__.append('BrandListView')


class ActualProductByBrandView(APIView):

    def get(self, request, brand_id):
        qs = ActualProduct.objects.filter(brand__id=brand_id)
        serializer = BrandSerializer(qs, many=True)
        return Response(serializer.data)


__all__.append('ActualProductByBrandView')


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
        selector_values = ProductTypeSelectorValue.objects.filter(id__in=selector_ids)
        serializer = ProductTypeSelectorValueSerializer(selector_values, many=True)
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
    serializer_class = ProductTypeSerializer
    filterset_class = ProductTypeFilter


class ProductTypeSelectorViewSet(NoDeleteModelViewSet):
    queryset = ProductTypeSelector.objects.all().order_by('-id')
    serializer_class = ProductTypeSelectorSerializer
    filterset_class = ProductTypeSelectorFilter

    @action(detail=False, methods=['get'])
    def get_by_list(self, request):
        ids = request.query_params.getlist('ids[]')
        qs = self.queryset.filter(pk__in=ids)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)


class ProductTypeSelectorValueViewSet(ReadOnlyModelViewSet):
    queryset = ProductTypeSelectorValue.objects.all().order_by('digikala_id')
    serializer_class = ProductTypeSelectorValueSerializer
    filterset_class = ProductTypeSelectorValueFilter

    @action(detail=False, methods=['get'])
    def get_by_list(self, request):
        ids = request.query_params.getlist('ids[]')
        qs = self.queryset.filter(pk__in=ids)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)


class ProductVariantViewSet(NoDeleteModelViewSet):
    queryset = ProductVariant.objects.all().order_by('-id')
    filterset_class = VariantFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductVariantSerializer
        return ProductVariantWriteSerializer


class InvoiceViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Invoice.objects.all().order_by('-start_date')
    serializer_class = InvoiceSerializer
    filterset_class = InvoiceFilter

    @action(detail=True, methods=['get'])
    def get_details(self, request, *args, **kwargs):
        invoice = self.get_object()
        items = invoice.invoice_items.all()
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

        data = [v for k, v in dkp_data.items()]
        return Response(data)


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


class DigiLoginCredentialsView(APIView):
    KEY_PASSWORD = 'digi_password'
    KEY_USERNAME = 'digi_username'

    def get(self, request):
        db = JsonDB()
        response = {
            self.KEY_USERNAME: db.get(self.KEY_USERNAME),
            self.KEY_PASSWORD: db.get(self.KEY_PASSWORD),
        }
        return Response(response)

    def post(self, request):
        db = JsonDB()
        username = request.data.get(self.KEY_USERNAME, db.get(self.KEY_USERNAME))
        password = request.data.get(self.KEY_PASSWORD, db.get(self.KEY_PASSWORD))
        db.set(self.KEY_USERNAME, username)
        db.set(self.KEY_PASSWORD, password)
        response = {
            self.KEY_USERNAME: username,
            self.KEY_PASSWORD: password,
        }
        return Response(response, status=status.HTTP_201_CREATED)


class ScrapeInvoiceView(APIView):

    def post(self, request):
        task = scrape_invoice_page.delay()
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class TestCelerySuccessTask(APIView):

    def post(self, request):
        task = just_sleep.delay()
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


__all__.append('TestCelerySuccessTask')


class TestCeleryFailTask(APIView):

    def post(self, request):
        task = just_sleep_and_fail.delay()
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


__all__.append('TestCeleryFailTask')


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
        # current = task.info.get('current', 0)
        # total = task.info.get('total', 1)
        # progression = (int(current) / int(total)) * 100  # to display a percentage of progress of the task
        response = {
            'task_id': task_id,
            'state':   task.state,
            # 'progression': progression,
            'info':    None
        }
        return Response(response, status=200)


class RobotVariantsFilterView(APIView):

    def get(self, request):
        actual_product_id = request.query_params.get('actual_product_id')
        selector_id = request.query_params.get('selector_id')
        print(f'{actual_product_id = } | {selector_id = }')
        variants = ProductVariant.objects.filter(
            selector_id=selector_id,
            actual_product_id=actual_product_id
        )
        print(variants)
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)


__all__.append('RobotVariantsFilterView')
