from dataclasses import dataclass


@dataclass
class FetchData:
    robot_is_on: bool
    robot_running: bool


@dataclass
class ToggleRobotData:
    robot_is_on: bool


@dataclass
class RobotRunningData:
    robot_running: bool
