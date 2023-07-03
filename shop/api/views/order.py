from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.serializers import *
from shop.queries import get_product_with_attrs
from utils.drf.permissions import IsAdmin, IsAuthenticated


__all__ = [
    'OrderViewSet',
]


class OrderViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Order.objects \
        .select_related('user') \
        .prefetch_related(Prefetch('items', queryset=OrderItem.objects.all())) \
        .all() \
        .order_by('id')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderReadSerializer
        return OrderWriteSerializer
