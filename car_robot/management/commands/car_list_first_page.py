from django.core.management import BaseCommand
from django.conf import settings

from car_robot.scrapers import *
from utils.logging import logger


PAGE_URL = 'https://divar.ir/s/tehran/car/samand/lx/ef7-petrol'


class Command(BaseCommand):

    def handle(self, *args, **options):
        robot = CarListScraper(PAGE_URL)
        links = robot.run()

        detail_robot = CarDetailScraper(links)
        detail_robot.run()
