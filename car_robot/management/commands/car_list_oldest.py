import time
import json

from django.core.management import BaseCommand

from car_robot.scrapers import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('old_ads.json', 'r', encoding='utf-8') as f:
            all_links = json.load(f)

        robot = CarDetailScraper(all_links[:100])
        robot.run()
