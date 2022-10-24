import copy
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import TypedDict

from users.models import User


class RequestType(TypedDict):
    command: int
    payload: dict
    req_key: str


class BaseCommand(ABC):
    """
    base class for Command classes
    """
    SENDER_RESPONSE_TYPE: str
    OTHERS_RESPONSE_TYPE: str

    def __init__(self, user_obj: User, group_name: str, client_type: str):
        self.user = user_obj
        self.group_name = group_name
        self.client_type = client_type

        self.request = None
        self.response_for_me = []
        self.response_for_others = defaultdict(list)

    @abstractmethod
    def respond(self, request: RequestType) -> None:
        """
        create response for the user and other users/groups
        """

    def get_response(self, request: RequestType) -> dict[str, list[dict]]:
        self.request = request
        self.response_for_me = []
        self.response_for_others = defaultdict(list)

        self.respond(request)

        response = {
            self.group_name: self.response_for_me
        }

        return response | self.response_for_others

    def add_response_for_me(
            self,
            data,
            msg_type: str = None,
            add_key: bool = True
    ) -> None:
        """
        for sending message to user websocket
        """
        res = {'data': data}

        if msg_type is None:
            res['type'] = self.SENDER_RESPONSE_TYPE
        else:
            res['type'] = msg_type

        if add_key is True:
            res['req_key'] = self.request.get('req_key')

        self.response_for_me.append(res)

    def add_response_for_others(self, groupname: str, data) -> dict:
        """
        for sending message to other users websocket
        """
        res = {
            'type': self.OTHERS_RESPONSE_TYPE,
            'data': data
        }

        self.response_for_others[groupname].append(res)

        return copy.deepcopy(res)


__all__ = [
    'RequestType',
    'BaseCommand',
]
