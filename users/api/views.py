from uuid import uuid4

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import User
from ..serializers import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None


def change_file_name(file_name: str):
    parts = file_name.split('.')
    extension = parts[-1]
    return f'{uuid4().hex}.{extension}'


class ProfileView(APIView):
    http_method_names = ['get', 'patch', 'options']

    def get(self, request):
        serializer = ProfileReadSerializer(request.user.profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileWriteSerializer(data=request.data, instance=profile, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
