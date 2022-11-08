from .commands.fetch import *
from .commands.toggle_robot import *
from .commands.webrtc import *


COMMAND_MAP = {
    1: FetchCommand,
    2: ToggleRobotStatusCommand,
    3: WebRTCSignalCommand,
    4: WebRTCAnswered,
}
