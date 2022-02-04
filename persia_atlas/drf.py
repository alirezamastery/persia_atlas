from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = None

    def get_paginated_response(self, data, *args, **kwargs):
        return Response({
            'next':       self.get_next_link(),
            'previous':   self.get_previous_link(),
            'count':      self.page.paginator.count,
            'page_count': self.page.paginator.num_pages,
            'items':      data,
            'extra_data': kwargs.get('extra_data')
        })
