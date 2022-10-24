import copy
from dataclasses import asdict

from django.core.cache import cache

from .base import *
from ..response import ResponseType
from ..response_data import ToggleRobotData
from ..constants import *
from persia_atlas.cache import CacheKey


class ToggleRobotStatusCommand(BaseCommand):
    SENDER_RESPONSE_TYPE = ResponseType.TOGGLE_ROBOT.value
    OTHERS_RESPONSE_TYPE = ResponseType.TOGGLE_ROBOT.value

    def respond(self, request: RequestType):
        payload = request['payload']
        robot_is_on = bool(payload.get('robot_is_on'))
        cache.set(CacheKey.ROBOT_IS_ON.value, robot_is_on, timeout=None)

        data = asdict(ToggleRobotData(robot_is_on=robot_is_on))

        self.add_response_for_me(data)

        self.add_response_for_others(
            groupname=ALL_USERS_GROUP,
            data=data
        )


__all__ = [
    'ToggleRobotStatusCommand'
]
