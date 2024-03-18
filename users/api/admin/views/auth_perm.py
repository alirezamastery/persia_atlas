from django.db.models import Q
from django.contrib.auth.models import Permission
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

from users.api.admin.serializers import *
from utils.drf.permissions import *
from utils.drf.mixins import *
from utils.drf.pagination import CustomPageNumberPagination


__all__ = [
    'AuthPermissionViewSetAdmin',
]

SHOW_CONTENTTYPES = [3, 4, 5, 6, 7, 8, 9, 10, 11, ]


class AuthPermissionViewSetAdmin(ModelViewSet, GetByIdList):
    queryset = (Permission.objects
                .filter(~Q(codename__contains='delete'))
                .order_by('-id'))
    permission_classes = [IsSuperuser]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AuthPermissionReadSerializerAdmin
        return AuthPermissionWriteSerializerAdmin
