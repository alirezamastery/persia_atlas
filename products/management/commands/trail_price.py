import traceback
from dataclasses import asdict

from django.core.cache import cache
from django.core.management import BaseCommand
from requests.exceptions import RequestException

from products.robot.robots.trail_price_v1 import TrailingPriceRobot
from utils.logging import get_tehran_datetime, logger
from products.websocket.utils import send_msg_websocket_group
from products.websocket.constants import *
from products.robot.exceptions import StopRobot
from products.websocket.response import ResponseType
from products.websocket.response_data import RobotRunningData
from persia_atlas.cache import CacheKey


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--dkp',
            action='store',
        )

    def handle(self, *args, **options):
        already_running = cache.get(CacheKey.ROBOT_RUNNING.value)
        if already_running:
            raise Exception('robot is already running')

        dkp = options.get('dkp')
        robot = TrailingPriceRobot(dkp=dkp)
        try:
            self.notify_robot_is_running(True)
            robot.run()
        except StopRobot:
            logger('ROBOT STOPPED')
        except RequestException:
            logger('there was a request exception')
        except:
            with open('robot_errors.txt', 'a', encoding='utf-8') as log_file:
                date = get_tehran_datetime()
                log_file.write(f'{date:-^100}\n')
                traceback.print_exc(file=log_file)
                log_file.write('\n' * 2)
                raise
        finally:
            self.notify_robot_is_running(False)

    @staticmethod
    def notify_robot_is_running(is_running: bool):
        cache.set(CacheKey.ROBOT_RUNNING.value, is_running, timeout=None)
        data = RobotRunningData(robot_running=is_running)
        send_msg_websocket_group(
            groupname=ALL_USERS_GROUP,
            msg_type=ResponseType.ROBOT_RUNNING.value,
            data=asdict(data),
        )
