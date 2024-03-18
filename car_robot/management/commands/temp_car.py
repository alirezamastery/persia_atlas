import time
import re
import random
from pprint import pprint

import requests
from django.core.management import BaseCommand
from django.conf import settings

from car_robot.scrapers import *
from utils.logging import logger
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
        cars = Car.objects.all()
        for car in cars:
            extract_date(car.time)
