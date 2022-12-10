from django.db.models import Min
from rest_framework.views import APIView
from rest_framework.response import Response
from khayyam import JalaliDatetime

from ..sql import *
from accounting.models import *
from accounting.api.serializers.sales import *
from utils.query import *


class SalesCountView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = SalesQueryParamSerializer(data={
            'ap_id': request.query_params.get('ap_id')
        })
        serializer.is_valid(raise_exception=True)
        actual_product = serializer.validated_data['actual_product']

        item_min_date = InvoiceItem.objects.aggregate(min=Min('date'))['min']
        start_j = JalaliDatetime(item_min_date)
        start_year = start_j.year
        start_month = start_j.month
        now = JalaliDatetime.now()
        now_year = now.year
        now_month = now.month
        j_months = []
        j_month = start_month
        j_year = start_year
        while j_year < now_year or (j_year == now_year and j_month < now_month):
            start = JalaliDatetime(j_year, j_month, 1)
            j_months.append(start)
            if j_month == 12:
                j_year += 1
                j_month = 1
            else:
                j_month += 1

        months = [j.todatetime() for j in j_months]

        response = {
            'actual_product': ActualProductSerializer(actual_product).data,
            'sales':          raw_query_auto_named(
                sql=SQL_ACTUAL_PRODUCT_SALES_BY_MONTH,
                params={'months': months, 'ap_id': serializer.validated_data['ap_id']}
            )
        }

        return Response(response)


__all__ = [
    'SalesCountView',
]
