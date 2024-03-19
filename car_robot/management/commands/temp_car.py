import time
import re
import random
from pprint import pprint

import requests
from django.core.management import BaseCommand
from django.conf import settings

from car_robot.scrapers import *
from utils.logging import logger
from car_robot.scrapers.laptop_detail import LaptopDetailScraper
from car_robot.models import *


time_map = {
    'هفته':   'week',
    'روز':    'day',
    'ساعت':   'hour',
    'دقایقی': 'minute',
    'لحظاتی': 'second',
}


def extract_date(time: str):
    value = None
    for val in time_map.keys():
        if val in time:
            print(val)
            break
    if value is None:
        raise RuntimeError(f'no mathc for time: {time}')

    amount = re.match('')



class Command(BaseCommand):

    def handle(self, *args, **options):
        urls = [
            '/v/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-rog-g533zm/AZZ_N-30'
        ]

        robot = LaptopDetailScraper(urls)
        robot.run()
