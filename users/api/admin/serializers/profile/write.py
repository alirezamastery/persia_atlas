from rest_framework import serializers

from users.models import Profile
from .read import ProfileReadSerializerAdmin


__all__ = [
    'ProfileWriteSerializerAdmin',
]


class ProfileWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'avatar',
        ]

    def to_representation(self, instance):
        return ProfileReadSerializerAdmin(instance, context=self.context).data
