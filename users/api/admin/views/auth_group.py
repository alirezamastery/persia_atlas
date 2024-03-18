from django.contrib.auth.models import Group
from rest_framework.permissions import SAFE_METHODS

from rest_framework.viewsets import ModelViewSet

from users.api.admin.serializers import *
from utils.drf.permissions import *
from utils.drf.mixins import *
from utils.drf.pagination import CustomPageNumberPagination


__all__ = [
    'AuthGroupViewSetAdmin',
]


class AuthGroupViewSetAdmin(ModelViewSet, GetByIdList):
    queryset = Group.objects.all().order_by('-id')
    permission_classes = [IsSuperuser]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AuthGroupReadSerializerAdmin
        return AuthGroupWriteSerializerAdmin
