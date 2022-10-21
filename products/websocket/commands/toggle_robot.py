import copy
from dataclasses import asdict

from django.core.cache import cache

from .base import *
from ..response_data import ToggleRobotData
from ..constants import *
from persia_atlas.cache import CacheKey


class ToggleRobotStatusCommand(BaseCommand):
    SENDER_RESPONSE_TYPE = ResponseType.TOGGLE_ROBOT.value
    OTHERS_RESPONSE_TYPE = ResponseType.TOGGLE_ROBOT.value

    def respond(self, payload: dict) -> dict:
        robot_is_on = bool(payload.get('robot_is_on'))
        cache.set(CacheKey.ROBOT_IS_ON.value, robot_is_on, timeout=None)
        data = ToggleRobotData(robot_is_on=robot_is_on)

        response_for_me = {
            'type': self.SENDER_RESPONSE_TYPE,
            'data': asdict(data)
        }

        return {
            USER_RESPONSE:   response_for_me,
            USER_CHANNEL:    self.group_name,
            OTHERS_RESPONSE: copy.deepcopy(response_for_me),
            OTHERS_CHANNEL:  ALL_USERS_GROUP,
        }


__all__ = [
    'ToggleRobotStatusCommand'
]
