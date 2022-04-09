from abc import ABC, abstractmethod

from users.models import User


class BaseCommand(ABC):
    """
    base class for Command classes
    """

    def __init__(self, user_obj: User, group_name: str):
        self.user = user_obj
        self.group_name = group_name

    @abstractmethod
    def respond(self, payload: dict) -> dict:
        """create response dictionary"""
