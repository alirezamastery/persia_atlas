from django.core.management import BaseCommand

from products.robot.robots import TrailingPriceRobot


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--tail',
            action='store',
        )

    def handle(self, *args, **options):
        tail = options.get('tail')
        robot = TrailingPriceRobot(tail=tail)
        robot.run()
