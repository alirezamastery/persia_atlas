from .base import *
from ..response import ResponseType
from ..exceptions import *
from ..utils import get_user_groupname


class WebRTCSignalCommand(BaseCommand):
    SENDER_RESPONSE_TYPE = ResponseType.WEBRTC_SIGNAL.value

    def respond(self, request: RequestType):
        payload = request['payload']
        signal_type = payload.get('type')
        if signal_type is None:
            raise InvalidClientPayload(f'signal type is required')

        self.add_response_for_others(
            groupname=get_user_groupname(payload['target']),
            data=payload
        )


__all__ = [
    'WebRTCSignalCommand',
]
