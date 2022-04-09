import traceback

from django.core.cache import cache
from django.conf import settings
from django.core.management import BaseCommand

# from products.robot.robots.trail_price_v0 import TrailingPriceRobot
from products.robot.robots.trail_price_v1 import TrailingPriceRobot
from utils.logging import get_tehran_datetime, logger
from products.websocket.utils import send_msg_websocket_group
from products.websocket.constants import *
from products.robot.exceptions import StopRobot


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--dkp',
            action='store',
        )

    def handle(self, *args, **options):
        dkp = options.get('dkp')
        robot = TrailingPriceRobot(dkp=dkp)
        try:
            cache.set(settings.CACHE_KEY_ROBOT_RUNNING, 'true', timeout=None)
            msg = {
                'robot_running': True
            }
            send_msg_websocket_group(ALL_USERS_GROUP, msg, msg_type='robot_status')
            robot.run()
        except StopRobot:
            logger('ROBOT STOPPED')
        except:
            with open('robot_errors.txt', 'a', encoding='utf-8') as log_file:
                date = get_tehran_datetime()
                log_file.write(f'{date:-^100}\n')
                traceback.print_exc(file=log_file)
                log_file.write('\n' * 2)
                raise
        finally:
            cache.set(settings.CACHE_KEY_ROBOT_RUNNING, 'false', timeout=None)
            msg = {
                'robot_running': False
            }
            send_msg_websocket_group(ALL_USERS_GROUP, msg, msg_type='robot_status')
