from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers


__all__ = [
    'OptionalPagination',
    'GetByIdList',
]


class OptionalPagination:

    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(self.paginator.page_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)


class GetByIdList:

    @action(detail=False, methods=['get'], url_path='get-by-id-list')
    def get_by_id_list(self, request):
        ids = request.query_params.getlist('ids[]')
        qs = self.queryset.filter(pk__in=ids)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

