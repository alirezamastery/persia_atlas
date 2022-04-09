from .commands.fetch import *
from .commands.stop_robot import *


COMMAND_MAP = {
    1: FetchCommand,
    2: StopRobotCommand,
}
