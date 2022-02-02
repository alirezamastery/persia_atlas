from rest_framework import serializers

from .models import User, Profile
from utils.serializer import lazy_serializer


class ProfileSerializer(serializers.ModelSerializer):
    # user = lazy_serializer('users.serializers.UserSerializer')(read_only=True) # TODO

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['mobile', 'profile']
