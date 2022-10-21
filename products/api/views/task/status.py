from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response


class CeleryTaskStateView(APIView):

    def get(self, request, task_id):
        task = AsyncResult(task_id)

        if task.state == 'FAILURE' or task.state == 'PENDING':
            response = {
                'task_id':     task_id,
                'state':       task.state,
                'progression': None,
                'info':        str(task.info)
            }
            return Response(response, status=200)
        response = {
            'task_id': task_id,
            'state':   task.state,
            'info':    None
        }
        return Response(response, status=200)


__all__ = [
    'CeleryTaskStateView',
]
