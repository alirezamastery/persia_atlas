from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.serializers import *
from products.tasks import scrape_invoice_page


class ScrapeInvoiceView(APIView):

    def post(self, request):
        serializer = ScrapeInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        row_number = serializer.validated_data['row_number']
        task = scrape_invoice_page.delay(row_number)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


__all__ = [
    'ScrapeInvoiceView'
]
