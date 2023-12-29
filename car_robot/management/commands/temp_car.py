import time
import random
from pprint import pprint

import requests
from django.core.management import BaseCommand
from django.conf import settings

from car_robot.scrapers import *
from utils.logging import logger
from car_robot.models import *


PAGE_URL = 'https://divar.ir/s/tehran/car/samand/lx/ef7-petrol'
DETAIL_URL = 'https://divar.ir/v/%D8%B3%D9%85%D9%86%D8%AF-lx-ef7-%D8%A8%D9%86%D8%B2%DB%8C%D9%86%DB%8C-%D9%85%D8%AF%D9%84-%DB%B1%DB%B3%DB%B9%DB%B6/QZGysoIO'


class Command(BaseCommand):

    def handle(self, *args, **options):
        # robot = CarDetailScraper([
        #     # '/v/%D8%B3%D9%85%D9%86%D8%AF-lx-ef7-%D8%A8%D9%86%D8%B2%DB%8C%D9%86%DB%8C-%D9%85%D8%AF%D9%84-%DB%B1%DB%B3%DB%B9%DB%B6/QZGysoIO',
        #     '/v/%D8%B3%D9%85%D9%86%D8%AF-ef7-%D9%85%D8%AF%D9%84-94/QZH2AIPk',
        # ])
        # try:
        #     robot.run()
        # finally:
        #     robot.clean_up()
        res = requests.get('https://persia-atlas.com/api/car-robot/cars/')
        pprint(res.json())