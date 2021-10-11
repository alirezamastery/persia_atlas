from django.core.management import BaseCommand

from products.robot.robots import TrailingPriceRobot


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--tail',
            action='store',
        )
        parser.add_argument(
            '--dkp',
            action='store',
        )

    def handle(self, *args, **options):
        tail = options.get('tail')
        dkp = options.get('dkp')
        robot = TrailingPriceRobot(dkp=dkp, tail=tail)
        robot.run()
