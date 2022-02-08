import datetime as dt

from django.conf import settings
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import status

from ...models import *
from ..serializers import *
from ..filters import *
from products.models import ProductVariant


class CostTypeViewSet(ModelViewSet):
    queryset = CostType.objects.all().order_by('-id')
    serializer_class = CostTypeSerializer
    filterset_class = CostTypeFilter


class CostViewSet(ModelViewSet):
    queryset = Cost.objects.all().order_by('-id')
    filterset_class = CostFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CostReadSerializer
        return CostWriteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            extra_data = queryset.aggregate(sum=Sum('amount'))
            # Access paginator directly to pass kwargs:
            return self.paginator.get_paginated_response(serializer.data, extra_data=extra_data)

        raise Exception('no paginator is set')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        today = dt.datetime.now(dt.timezone.utc).astimezone()
        delta = today - instance.created_at
        max_days = settings.MAX_DAYS_DELETE_COST
        if delta.days > max_days:
            return Response({'error': f'can not delete cost after {max_days} days'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IncomeViewSet(ModelViewSet):
    queryset = Income.objects.all().order_by('-id')
    serializer_class = IncomeSerializer
    filterset_class = IncomeFilter


class ProductCostViewSet(ModelViewSet):
    queryset = ProductCost.objects.all().order_by('-id')
    serializer_class = ProductCostSerializer
    filterset_class = ProductCostFilter


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


__all__ = [
    'CostTypeViewSet',
    'CostViewSet',
    'IncomeViewSet',
    'ProductCostViewSet',
    'InvoiceViewSet',
    'InvoiceItemViewSet'
]
