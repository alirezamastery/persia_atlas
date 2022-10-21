from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import status

from ...models import *
from ..serializers import *
from ..filters import *
from ..sql import *
from utils.query import execute_raw_query


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
        params = {'invoice_id': invoice.id}
        result = execute_raw_query(sql=SQL_INVOICE_ACTUAL_PRODUCT_COUNT, params=params)
        total_count = result[0][-1]
        items = [{
            'row_number':        row[0],
            'actual_product_id': row[1],
            'title':             row[2],
            'count':             row[3],
        } for row in result]

        response = {
            'items':       items,
            'total_count': total_count
        }
        return Response(response)


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
    'InvoiceViewSet',
    'InvoiceItemViewSet'
]
