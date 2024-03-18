from rest_framework import serializers

from django.contrib.auth.models import Permission


__all__ = [
    'AuthPermissionReadSerializerAdmin',
    'AuthPermissionWriteSerializerAdmin',
]


class AuthPermissionReadSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class AuthPermissionWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'codename']
