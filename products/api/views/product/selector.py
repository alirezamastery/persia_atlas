from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from products.models import *
from products.serializers import *
from products.api.filters import *


class VariantSelectorTypeViewSet(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 GenericViewSet):
    queryset = VariantSelectorType.objects.all().order_by('-id')
    serializer_class = VariantSelectorTypeSerializer
    filterset_class = VariantSelectorTypeFilter

    @action(detail=False, methods=['get'], url_path='get-by-id-list')
    def get_by_id_list(self, request):
        ids = request.query_params.getlist('ids[]')
        qs = self.queryset.filter(pk__in=ids)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)


class VariantSelectorViewSet(ReadOnlyModelViewSet):
    queryset = VariantSelector.objects.all().order_by('digikala_id')
    serializer_class = VariantSelectorSerializer
    filterset_class = VariantSelectorFilter

    @action(detail=False, methods=['get'], url_path='get-by-id-list')
    def get_by_id_list(self, request):
        ids = request.query_params.getlist('ids[]')
        qs = self.queryset.filter(pk__in=ids)
        serializer = self.get_serializer_class()(qs, many=True)
        return Response(serializer.data)


__all__ = [
    'VariantSelectorTypeViewSet',
    'VariantSelectorViewSet',
]
