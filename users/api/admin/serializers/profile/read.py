from rest_framework import serializers

from users.models import *
from utils.cache import get_user_status


__all__ = [
    'ProfileReadSerializerAdmin',
    'ProfileWriteSerializerAdmin',
    'UserSerializerAdmin',
]


class ProfileReadSerializerAdmin(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(method_name='get_avatar_full_url')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar']

    def get_avatar_full_url(self, obj):
        if not obj.avatar:
            return None
        avatar_url = obj.avatar.url
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(avatar_url)
        if (host := self.context.get('host')) is not None:
            return f'{host}{avatar_url}'
        return avatar_url


class ProfileWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar']

    def to_representation(self, instance):
        return ProfileReadSerializerAdmin(instance, context=self.context).data


class UserSerializerAdmin(serializers.ModelSerializer):
    profile = ProfileWriteSerializerAdmin(read_only=True)

    class Meta:
        model = User
        fields = ['mobile', 'profile']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['is_online'] = get_user_status(instance.id)
        return response
