from django.contrib.auth.models import Permission, Group
from rest_framework import serializers

from users.models import Profile


class _ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class _AuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class _AuthGroupSerializer(serializers.ModelSerializer):
    permissions = _AuthPermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']
