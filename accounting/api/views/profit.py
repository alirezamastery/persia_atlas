import datetime as dt

from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from khayyam import JalaliDate

from ...models import *
from ..serializers import *
from utils.date import *


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


class YearProfitView(APIView):

    def get(self, request):
        try:
            j_year = int(request.query_params.get('j_year'))
        except:
            today = JalaliDate.today()
            j_year = today.year

        print(f'{j_year = }')

        profits = []
        for month in range(1, 13):
            first_day = month_first_day(j_year, month)
            last_day = month_last_day(j_year, month)
            print(first_day)
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
            profits.append(profit)

        data = {
            'j_year':  j_year,
            'profits': profits
        }

        return Response({'data': data})
