from dataclasses import asdict

from django.core.cache import cache

from .base import *
from ..constants import *
from ..response_data import FetchData
from utils.logging import plogger
from persia_atlas.cache import CacheKey


class FetchCommand(BaseCommand):
    SENDER_RESPONSE_TYPE = ResponseType.FETCH.value

    def respond(self, payload: dict) -> dict:
        data = FetchData(
            robot_is_on=bool(cache.get(CacheKey.ROBOT_IS_ON.value)),
            robot_running=bool(cache.get(CacheKey.ROBOT_RUNNING.value))
        )
        response_for_me = {
            'type': self.SENDER_RESPONSE_TYPE,
            'data': asdict(data)
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
