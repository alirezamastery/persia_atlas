from django.db.models import Sum, OuterRef, Subquery, Value, Prefetch, Min, Max
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action

from shop.models import *
from shop.serializers import *
from shop.api.filters import *
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'ProductViewSetPublic',
    'ProductViewSetAdmin',
]


class ProductViewSetPublic(ReadOnlyModelViewSet):
    permission_classes = [ReadOnly]
    filterset_class = ProductFilterPublic

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializerPublic
        return ProductDetailSerializerPublic

    def get_queryset(self):
        prefetch_variants = Prefetch(
            'variants',
            queryset=Variant.objects
                .filter(is_active=True)
                .select_related('selector_value__type')
                .order_by('created_at')
        )

        if self.action == 'list':
            total_inv_subq = Variant.objects \
                .values('product_id') \
                .filter(product=OuterRef('id')) \
                .annotate(sum=Sum('inventory')) \
                .values('sum')
            min_price_subq = Variant.objects \
                .values('product_id') \
                .filter(product=OuterRef('id')) \
                .annotate(min=Min('price')) \
                .values('min')
            return Product.objects \
                .select_related('brand') \
                .select_related('category') \
                .prefetch_related(prefetch_variants) \
                .filter(is_active=True) \
                .annotate(total_inventory=Coalesce(Subquery(total_inv_subq), Value(0))) \
                .annotate(price_min=Subquery(min_price_subq)) \
                .order_by('id')

        prefetch_attrs = Prefetch(
            'attribute_values',
            queryset=ProductAttributeValue.objects.select_related('attribute')
        )
        return Product.objects \
            .select_related('brand') \
            .select_related('category') \
            .prefetch_related(prefetch_variants) \
            .prefetch_related(prefetch_attrs) \
            .filter(is_active=True) \
            .order_by('id')

    @action(detail=False, methods=['GET'], url_path='get-price-range')
    def get_price_range(self, request):
        # min_price_subq = Variant.objects \
        #     .values('product_id') \
        #     .filter(product=OuterRef('id')) \
        #     .annotate(min=Min('price')) \
        #     .values('min')
        # price_min = Product.objects \
        #                 .filter(is_active=True) \
        #                 .annotate(price_min=Subquery(min_price_subq)) \
        #                 .aggregate(min=Min('price_min'))['min'] or 0

        max_price_subq = Variant.objects \
            .values('product_id') \
            .filter(product=OuterRef('id')) \
            .annotate(max=Max('price')) \
            .values('max')
        price_max = Product.objects \
                        .filter(is_active=True) \
                        .annotate(price_max=Subquery(max_price_subq)) \
                        .aggregate(max=Max('price_max'))['max'] or 0

        response = {
            'min': 0,
            'max': price_max,
        }
        return Response(response)


class ProductViewSetAdmin(ModelViewSet):
    filterset_class = ProductFilterAdmin
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializerAdmin
        if self.action == 'retrieve':
            return ProductDetailSerializerAdmin
        return ProductWriteSerializerAdmin

    def get_queryset(self):
        if self.action == 'list':
            return Product.objects \
                .select_related('brand') \
                .select_related('category') \
                .all() \
                .order_by('id')

        prefetch_attrs = Prefetch(
            'attribute_values',
            queryset=ProductAttributeValue.objects.select_related('attribute')
        )
        return Product.objects \
            .select_related('brand') \
            .select_related('category') \
            .prefetch_related('variants__selector_value__type') \
            .prefetch_related(prefetch_attrs) \
            .all() \
            .order_by('id')

    @action(detail=False, methods=['POST'], url_path='add-variants')
    def add_variants(self, request, *args, **kwargs):
        serializer = VariantCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
