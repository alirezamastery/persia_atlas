from rest_framework.viewsets import ModelViewSet

from ...models import Income
from ..serializers import IncomeSerializer
from ..filters import IncomeFilter


class IncomeViewSet(ModelViewSet):
    queryset = Income.objects.all().order_by('-id')
    serializer_class = IncomeSerializer
    filterset_class = IncomeFilter


__all__ = [
    'IncomeViewSet',
]
