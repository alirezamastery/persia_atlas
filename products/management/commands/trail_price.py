from django.core.management import BaseCommand

# from products.robot.robots.trail_price_v0 import TrailingPriceRobot
from products.robot.robots.trail_price_v1 import TrailingPriceRobot


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
        robot.run()
