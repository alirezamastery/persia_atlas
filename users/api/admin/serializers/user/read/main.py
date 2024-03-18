from rest_framework import serializers

from users.models import User

from users.api.admin.serializers.profile.read import ProfileReadSerializerAdmin
from ._sub import (
    _AuthPermissionSerializer,
    _AuthGroupSerializer,
)

__all__ = [
    'UserReadSerializerAdmin'
]


class UserReadSerializerAdmin(serializers.ModelSerializer):
    profile = ProfileReadSerializerAdmin(read_only=True)
    auth_groups = serializers.SerializerMethodField(method_name='get_auth_groups')
    user_permissions = _AuthPermissionSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'mobile',
            'is_active',
            'is_staff',
            'is_superuser',

            'profile',
            'auth_groups',
            'user_permissions',
        ]

    def get_auth_groups(self, obj: User):
        return _AuthGroupSerializer(obj.groups.all(), many=True, context=self.context).data
