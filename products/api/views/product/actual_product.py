from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from products.models import *
from products.serializers import *
from products.api.filters import *


class ActualProductByBrandView(APIView):

    def get(self, request, brand_id):
        qs = ActualProduct.objects.filter(brand__id=brand_id)
        serializer = BrandSerializer(qs, many=True)
        return Response(serializer.data)


class ActualProductViewSet(ModelViewSet):
    queryset = ActualProduct.objects.all().order_by('-id')
    serializer_class = ActualProductSerializer
    filterset_class = ActualProductFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActualProductSerializer
        return ActualProductWriteSerializer

    @action(detail=True, methods=['get'], url_path='related-selectors')
    def related_selectors(self, request, pk=None):
        actual_product = self.get_object()
        variants = actual_product.variants.all()
        selector_ids = []
        for var in variants:
            selector_ids.append(var.selector.id)
        selector_ids = set(selector_ids)
        selector_values = VariantSelector.objects.filter(id__in=selector_ids)
        serializer = VariantSelectorSerializer(selector_values, many=True)
        return Response(serializer.data)


__all__ = [
    'ActualProductByBrandView',
    'ActualProductViewSet',
]
