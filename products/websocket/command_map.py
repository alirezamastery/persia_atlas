from .commands.fetch import *
from .commands.stop_robot import *
from .commands.webrtc import *


COMMAND_MAP = {
    1: FetchCommand,
    2: StopRobotCommand,
    3: WebRTCSignalCommand,
}
