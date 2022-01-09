from uuid import uuid4

from django.core.files.storage import default_storage
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from ..models import User, Profile
from ..serializers import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def change_file_name(file_name: str):
    parts = file_name.split('.')
    extension = parts[-1]
    return f'{uuid4().hex}.{extension}'


class ProfileView(APIView):
    http_method_names = ['get', 'patch', 'options']

    def get(self, request):
        print('profile', request.user.profile)
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(data=request.data, instance=profile)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
