from dataclasses import asdict

from django.core.cache import cache

from .base import *
from ..response import ResponseType
from ..response_data import FetchData
from persia_atlas.cache import CacheKey


class FetchCommand(BaseCommand):
    SENDER_RESPONSE_TYPE = ResponseType.FETCH.value

    def respond(self, request: RequestType):
        data = FetchData(
            robot_is_on=bool(cache.get(CacheKey.ROBOT_IS_ON.value)),
            robot_running=bool(cache.get(CacheKey.ROBOT_RUNNING.value))
        )
        self.add_response_for_me(asdict(data))


__all__ = [
    'FetchCommand'
]
