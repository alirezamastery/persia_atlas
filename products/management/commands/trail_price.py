from django.core.management import BaseCommand

from products.robot.robots import TrailingPriceRobot


class Command(BaseCommand):

    def handle(self, *args, **options):
        robot = TrailingPriceRobot()
        robot.run()
