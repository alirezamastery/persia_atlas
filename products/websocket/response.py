from enum import Enum


class ResponseType(Enum):
    FETCH = 'fetch_response'
    TOGGLE_ROBOT = 'toggle_robot'
    ROBOT_RUNNING = 'robot_running'

    WEBRTC_SIGNAL = 'webrtc_signal'

    USER_STATUS = 'user_status'


__all__ = [
    'ResponseType'
]
