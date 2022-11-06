from colored import fg, attr
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .constants import *
from utils.logging import plogger, logger


def clr_print(*args):
    print(fg('green'), *args, attr('reset'))


def get_user_groupname(mobile: str) -> str:
    return f'{NAMEDGROUP_USER}{mobile}'


def get_group_groupname(group_id):
    return f'{NAMEDGROUP_GROUP}{group_id}'


def send_msg_websocket_group(groupname: str, msg_type: str, data: dict):
    socket_message = {
        'type': msg_type,
        'data': data
    }
    # plogger(socket_message)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        groupname,
        {
            'type':    'send_group_message',
            'mobile':  '',
            'message': socket_message
        }
    )
