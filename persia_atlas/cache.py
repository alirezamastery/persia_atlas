from enum import Enum


class CacheKey(Enum):
    ROBOT_IS_ON = 'robot_is_on'
    ROBOT_RUNNING = 'robot_running'

    ONLINE_USERS = 'online_users'
