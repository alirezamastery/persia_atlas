import datetime as dt

from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..models import Cost, CostType
from .serializers import CostSerializer, CostTypeSerializer


class CostTypeViewSet(ModelViewSet):
    queryset = CostType.objects.all().order_by('-id')
    serializer_class = CostTypeSerializer


class CostViewSet(ModelViewSet):
    queryset = Cost.objects.all().order_by('-id')
    serializer_class = CostSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        today = dt.datetime.now(dt.timezone.utc).astimezone()
        delta = today - instance.created_at
        max_days = settings.MAX_DAYS_DELETE_COST
        if delta.days > max_days:
            return Response({'error': f'can not delete cost after {max_days} days'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
