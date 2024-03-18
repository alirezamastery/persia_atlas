from rest_framework import serializers

from users.models import User
from .read.main import UserReadSerializerAdmin


__all__ = [
    'UserWriteSerializerAdmin',
    'PasswordResetSerializer',
]


class UserWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'is_staff',
            'is_active',
            'is_superuser',
            'user_permissions',
            'groups'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        return UserReadSerializerAdmin(instance).data


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, max_length=20, trim_whitespace=True)
