import datetime as dt

from django.conf import settings
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework import status

from ...models import *
from ..filters.car import *
from car_robot.api.serializers.car import *


__all__ = [
    'CarViewSet',
]


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all().order_by('price', 'kilometer', '-year')
    filterset_class = CarFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CarReadSerializer
        return CarWriteSerializer
