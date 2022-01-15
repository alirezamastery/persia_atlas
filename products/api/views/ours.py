from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from products.models import *
from products.serializers import *
from products.api.filters import *


__all__ = [
    'BrandViewSet', 'ActualProductViewSet', 'ProductViewSet', 'ProductTypeViewSet', 'ProductTypeSelectorViewSet',
    'ProductTypeSelectorValueViewSet', 'ProductVariantViewSet', 'InvoiceViewSet', 'InvoiceItemViewSet'
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


class ActualProductViewSet(NoDeleteModelViewSet):
    queryset = ActualProduct.objects.all().order_by('-id')
    serializer_class = ActualProductSerializer
    filterset_class = ActualProductFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActualProductSerializer
        return ActualProductWriteSerializer


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


class ProductTypeSelectorValueViewSet(ReadOnlyModelViewSet):
    queryset = ProductTypeSelectorValue.objects.all().order_by('digikala_id')
    serializer_class = ProductTypeSelectorValueSerializer
    filterset_class = ProductTypeSelectorValueFilter


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
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


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
