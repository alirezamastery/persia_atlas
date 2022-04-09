from django.core.cache import cache
from django.conf import settings

from .base import BaseCommand
from ..constants import *
from utils.logging import plogger


class FetchCommand(BaseCommand):

    def respond(self, payload: dict) -> dict:
        if cache.get(settings.CACHE_KEY_ROBOT_RUNNING) == 'true':
            robot_running = True
        else:
            robot_running = False

        if cache.get(settings.CACHE_KEY_STOP_ROBOT) == 'true':
            robot_is_on = False
        else:
            robot_is_on = True

        date = {
            'robot_running': robot_running,
            'robot_is_on':   robot_is_on,
        }

        response_for_me = {
            'type': 'fetch_response',
            'data': date
        }
        response = {
            USER_RESPONSE: response_for_me,
            USER_CHANNEL:  self.group_name,
        }
        plogger(response)
        return response


__all__ = [
    'FetchCommand'
]
