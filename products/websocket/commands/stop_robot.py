import copy

from django.core.cache import cache
from django.conf import settings

from .base import BaseCommand
from ..constants import *


class StopRobotCommand(BaseCommand):

    def respond(self, payload: dict) -> dict:
        stop = payload.get('stop')
        if stop is True:
            cache.set(settings.CACHE_KEY_STOP_ROBOT, 'true', timeout=None)
        else:
            cache.set(settings.CACHE_KEY_STOP_ROBOT, 'false', timeout=None)

        response_for_me = {
            'type': 'robot_stopped',
            'data': {
                'robot_is_on': not stop
            },
        }

        return {
            USER_RESPONSE:   response_for_me,
            USER_CHANNEL:    self.group_name,
            OTHERS_RESPONSE: copy.deepcopy(response_for_me),
            OTHERS_CHANNEL:  ALL_USERS_GROUP,
        }


__all__ = [
    'StopRobotCommand'
]
