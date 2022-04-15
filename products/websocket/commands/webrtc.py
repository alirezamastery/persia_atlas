from .base import BaseCommand
from ..constants import *
from ..exceptions import *
from ..utils import get_user_groupname


class WebRTCSignalCommand(BaseCommand):

    def respond(self, payload: dict) -> dict:
        signal_type = payload.get('type')
        if signal_type is None:
            raise InvalidClientPayload(f'signal type is required')

        response_for_other = {
            'type': 'webrtc_signal',
            'data': payload
        }

        return {
            OTHERS_RESPONSE: response_for_other,
            OTHERS_CHANNEL:  get_user_groupname(payload['target']),
        }


__all__ = [
    'WebRTCSignalCommand',
]
