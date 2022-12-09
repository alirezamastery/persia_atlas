import datetime as dt

from django.conf import settings
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from ...models import *
from accounting.api.serializers.accounting import *
from ..filters import *


class CostTypeViewSet(ModelViewSet):
    queryset = CostType.objects.all().order_by('-id')
    serializer_class = CostTypeSerializer
    filterset_class = CostTypeFilter


class CostViewSet(ModelViewSet):
    queryset = Cost.objects.all().order_by('-date')
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


class ProductCostViewSet(ModelViewSet):
    queryset = ProductCost.objects.all().order_by('-id')
    serializer_class = ProductCostSerializer
    filterset_class = ProductCostFilter


__all__ = [
    'CostTypeViewSet',
    'CostViewSet',
    'ProductCostViewSet',
]
