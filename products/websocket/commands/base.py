from abc import ABC, abstractmethod
from enum import Enum

from users.models import User


class ResponseType(Enum):
    FETCH = 'fetch_response'
    TOGGLE_ROBOT = 'toggle_robot'
    ROBOT_RUNNING = 'robot_running'


class BaseCommand(ABC):
    """
    base class for Command classes
    """
    SENDER_RESPONSE_TYPE: str
    OTHERS_RESPONSE_TYPE: str

    def __init__(self, user_obj: User, group_name: str):
        self.user = user_obj
        self.group_name = group_name

    @abstractmethod
    def respond(self, payload: dict) -> dict:
        """create response dictionary"""


__all__ = [
    'ResponseType',
    'BaseCommand',
]
