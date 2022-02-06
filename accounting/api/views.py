import datetime as dt

from django.conf import settings
from django.db.models import Sum
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from khayyam import JalaliDate

from ..models import *
from .serializers import *
from .filters import *


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


class ProfitView(APIView):

    def get(self, request):
        serializer = JalaliDateSerializer(data={
            'j_year':  request.query_params.get('j_year'),
            'j_month': request.query_params.get('j_month'),
        })
        serializer.is_valid(raise_exception=True)

        j_year = serializer.validated_data.get('j_year')
        j_month = serializer.validated_data.get('j_month')
        first_day = JalaliDate(j_year, j_month, 1).todate()
        if j_month == 12:
            next_month_first_day = JalaliDate(j_year + 1, 1, 1)
        else:
            next_month_first_day = JalaliDate(j_year, j_month + 1, 1)
        j_last_day = next_month_first_day - dt.timedelta(days=1)
        last_day = j_last_day.todate()

        costs = Cost.objects \
                    .filter(date__gte=first_day, date__lte=last_day) \
                    .aggregate(sum=Sum('amount'))['sum'] or 0
        incomes = Income.objects \
                      .filter(date__gte=first_day, date__lte=last_day) \
                      .aggregate(sum=Sum('amount'))['sum'] or 0
        product_costs = ProductCost.objects \
                            .filter(date__gte=first_day, date__lte=last_day) \
                            .aggregate(sum=Sum('amount'))['sum'] or 0
        profit = incomes - costs - product_costs
        response = {
            'costs':         costs,
            'incomes':       incomes,
            'product_costs': product_costs,
            'profit':        profit
        }
        return Response(response)


__all__ = [
    'CostTypeViewSet',
    'CostViewSet',
    'IncomeViewSet',
    'ProductCostViewSet',
    'ProfitView'
]
