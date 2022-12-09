from rest_framework.viewsets import ModelViewSet

from ...models import Income
from accounting.api.serializers.accounting import IncomeSerializer
from ..filters import IncomeFilter


class IncomeViewSet(ModelViewSet):
    queryset = Income.objects.all().order_by('-date')
    serializer_class = IncomeSerializer
    filterset_class = IncomeFilter


__all__ = [
    'IncomeViewSet',
]
