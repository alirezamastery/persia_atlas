from rest_framework import serializers

from django.contrib.auth.models import Group, Permission


__all__ = [
    'AuthGroupReadSerializerAdmin',
    'AuthGroupWriteSerializerAdmin',
]


class _AuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class AuthGroupReadSerializerAdmin(serializers.ModelSerializer):
    permissions = _AuthPermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


class AuthGroupWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def to_representation(self, instance):
        return AuthGroupReadSerializerAdmin(instance).data
