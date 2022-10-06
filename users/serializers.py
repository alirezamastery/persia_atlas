from rest_framework import serializers

from .models import User, Profile
from utils.serializer import lazy_serializer


class ProfileReadSerializer(serializers.ModelSerializer):
    # user = lazy_serializer('users.serializers.UserSerializer')(read_only=True) # TODO
    avatar = serializers.SerializerMethodField(method_name='get_avatar_full_url')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar']

    def get_avatar_full_url(self, obj):
        if not obj.avatar:
            return None
        avatar_url = obj.avatar.url
        request = self.context.get('request')
        if request is None:
            return avatar_url
        return request.build_absolute_uri(avatar_url)


class ProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar']

    def to_representation(self, instance):
        return ProfileReadSerializer(instance, context=self.context).data


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileWriteSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['mobile', 'profile']


__all__ = [
    'ProfileReadSerializer',
    'ProfileWriteSerializer',
    'UserSerializer'
]
