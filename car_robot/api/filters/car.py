from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter

from car_robot.models import *


__all__ = [
    'CarFilter',
]


class CarFilter(filters.FilterSet):
    q = filters.CharFilter(method='search_in_fields')

    class Meta:
        model = Car
        fields = ['q']

    def search_in_fields(self, qs, name, value):
        return qs.filter(
            Q(title__contains=value) | Q(phone__contains=value) | Q(location__contains=value)
        )
