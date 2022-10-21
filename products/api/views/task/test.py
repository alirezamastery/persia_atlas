from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.tasks import just_sleep, just_sleep_and_fail


class TestCelerySuccessTask(APIView):

    def post(self, request):
        task = just_sleep.delay()
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class TestCeleryFailTask(APIView):

    def post(self, request):
        task = just_sleep_and_fail.delay()
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


__all__ = [
    'TestCeleryFailTask',
    'TestCelerySuccessTask',
]
