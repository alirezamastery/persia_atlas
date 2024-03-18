from django.db.models import Q, F
from django_filters import rest_framework as filters

from users.models import *


__all__ = [
    'UserFilterAdmin',
]


class UserFilterAdmin(filters.FilterSet):
    q = filters.CharFilter(method='search_user')
    is_active = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = User
        fields = ['q', 'is_active']

    def search_user(self, qs, name, value):
        return qs.filter(
            Q(profile__first_name__icontains=value)
            | Q(profile__last_name__icontains=value)
            | Q(username__icontains=value)
        )
