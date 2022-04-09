import inspect
from datetime import datetime
import pytz
from zoneinfo import ZoneInfo
from pprint import pformat
from textwrap import indent

from django.conf import settings

from colored import fg, bg, attr


DATE_STR_WIDTH = 20
CALLER_NAME_WIDTH = 30
SPACES = 2
LOG_KEY_WIDTH = DATE_STR_WIDTH + CALLER_NAME_WIDTH + SPACES
LOG_VALUE_WIDTH = 60
# LINE_SEPARATOR = ''.join(('─' * LOG_KEY_WIDTH, '┼', '─' * LOG_VALUE_WIDTH))
LINE_SEPARATOR = ''.join(('─' * LOG_KEY_WIDTH, '─', '─' * LOG_VALUE_WIDTH))
DELIMITER = '│'
# RESET = attr('reset')
RESET = ''


def get_call_stack_info():
    """
    call_stack[0] is this function itself
    call_stack[1] is the function that called this function. (logger and plogger)
    call_stack[2] is what called the logger or plogger
    """
    call_stack = inspect.stack()
    caller = call_stack[2].function[:CALLER_NAME_WIDTH]
    _self = call_stack[2][0].f_locals.get('self', None)
    user_id = None
    if _self:
        user = getattr(_self, 'user', None)
        if user:
            user_id = getattr(user, 'id', None)

    return caller, user_id


def get_tehran_datetime():
    now = datetime.now()
    tehran_zone = pytz.timezone('Asia/Tehran')
    tehran_dt = now.astimezone(tehran_zone)
    return tehran_dt.strftime('%Y-%m-%d  %H:%M:%S')


def logger(*args, color: str = '', bg_color: str = ''):
    if not settings.CUSTOM_LOGGING:
        return

    caller, user_id = get_call_stack_info()
    date = get_tehran_datetime()
    style = ''
    # if color:
    #     style += fg(color)
    # if bg_color:
    #     style += bg(bg_color)

    print(f'{date} {caller:>{CALLER_NAME_WIDTH}} {DELIMITER}{style}', *args, RESET)
    if user_id is not None:
        print(f'{f"user_id: {user_id}":>{LOG_KEY_WIDTH - 1}} {DELIMITER} ')
    print(LINE_SEPARATOR)


def plogger(data_obj, color: str = '', bg_color: str = ''):
    if not settings.CUSTOM_LOGGING:
        return

    caller, user_id = get_call_stack_info()
    date = get_tehran_datetime()
    style = ''
    # if color:
    #     style += fg(color)
    # if bg_color:
    #     style += bg(bg_color)
    indent_str = ' ' * LOG_KEY_WIDTH + DELIMITER
    lines = indent(pformat(data_obj), indent_str).splitlines()
    # first_line = lines.pop(0)
    # print(f'{date} {caller:>{CALLER_NAME_WIDTH}} {DELIMITER} {style}{first_line[LOG_KEY_WIDTH + 1:]}{RESET}')
    print(f'{date} {caller:>{CALLER_NAME_WIDTH}} {DELIMITER}')
    for i, line in enumerate(lines):
        if user_id and i == 0:
            print(
                f'{f"user_id: {user_id}":>{LOG_KEY_WIDTH - 1}} {DELIMITER}'
                f'{style}{line[LOG_KEY_WIDTH + 1:]}{RESET}'
            )
        else:
            print(f'{line[:LOG_KEY_WIDTH + 1]}{style}{line[LOG_KEY_WIDTH + 1:]}{RESET}')
    print(LINE_SEPARATOR)


def plogger_flat(data_obj: dict, color: str = 'light_gray', bg_color: str = ''):
    caller = get_call_stack_info()
    date = get_tehran_datetime()
    style = ''
    # if color:
    #     style += fg(color)
    # if bg_color:
    #     style += bg(bg_color)
    indent_str = ' ' * LOG_KEY_WIDTH + DELIMITER
    max_key_len = max(len(str(key)) for key in data_obj)
    key_format = lambda key: f'{f"{key}:":<{max_key_len + 1}}'
    for i, (key, value) in enumerate(data_obj.items()):
        if i == 0:
            print(f'{date} {caller:>{CALLER_NAME_WIDTH}} {DELIMITER} {style}{key_format(key)} {value}{RESET}')
        else:
            print(f'{indent_str} {style}{key_format(key)} {value}{RESET}')
    print(LINE_SEPARATOR)
