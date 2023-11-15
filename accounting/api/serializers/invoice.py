from rest_framework.serializers import ModelSerializer

from accounting.models import *


__all__ = [
    'InvoiceSerializer',
    'InvoiceItemSerializer',
    'InvoiceActualItemWriteSerializer',
]


class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceItemSerializer(ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'


class InvoiceActualItemWriteSerializer(ModelSerializer):
    class Meta:
        model = InvoiceActualItem
        fields = [
            'invoice',
            'actual_product',
            'quantity',
            'price',
        ]
