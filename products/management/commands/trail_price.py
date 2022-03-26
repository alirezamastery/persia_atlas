import traceback

from django.core.management import BaseCommand

# from products.robot.robots.trail_price_v0 import TrailingPriceRobot
from products.robot.robots.trail_price_v1 import TrailingPriceRobot
from utils.logging import get_tehran_datetime


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
            robot.run()
        except:
            with open('robot_errors.txt', 'a', encoding='utf-8') as log_file:
                date = get_tehran_datetime()
                log_file.write(f'{date:-^100}\n')
                traceback.print_exc(file=log_file)
                log_file.write('\n' * 2)
                raise
