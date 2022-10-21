from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.serializers import *
from persia_atlas.cache import CacheKey
from utils.logging import logger, plogger


class RobotStatusView(APIView):

    def get(self, request):
        running = bool(cache.get(CacheKey.ROBOT_IS_ON.value))
        return Response({'running': running})

    def post(self, request):
        serializer = RobotStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        robot_is_on = serializer.data.get('robot_is_on')
        logger(f'ROBOT IS ON: {robot_is_on}')
        cache.set(CacheKey.ROBOT_IS_ON.value, robot_is_on, timeout=None)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


__all__ = [
    'RobotStatusView'
]
