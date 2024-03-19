import json
import time
import random
import pickle
from pprint import pprint

import requests
from django.conf import settings
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from unidecode import unidecode

from car_robot.models import *
from utils.logging import logger


__all__ = [
    'LaptopDetailScraper',
]


def random_sleep(seconds: int = 1, gap: int = 1):
    time.sleep(round(random.uniform(seconds, seconds + gap), 2))


class LaptopDetailScraper:

    def __init__(self, urls: list[str]):
        self.urls = urls
        firefox_options = FirefoxOptions()
        firefox_options.headless = False
        firefox_options.binary_location = settings.FIREFOX_BINARY
        self.table_rows = []
        service = Service(settings.GECKO_DRIVER_PATH)
        self.browser = Firefox(service=service, options=firefox_options)
        self.site_base = 'https://divar.ir'
        self.found = []

    def run(self):
        logger('start')
        self.browser.get(self.site_base)
        for url in self.urls:
            self.extract_car_detail(url)

        with open('./found_laptop.json', 'w', encoding='utf-8') as f:
            json.dump(self.found, f, ensure_ascii=False)

        with open('./found_laptop.txt', 'w', encoding='utf-8') as f:
            for link in self.found:
                f.write(link)
                f.write('\n')

    def extract_car_detail(self, url):
        details = {}

        url_parts = url.split('/')
        token = url_parts[-1]
        try:
            Car.objects.get(token=token)
            logger(f'ALREADY EXISTS: {token}')
            return
        except:
            pass
        details['token'] = token

        full_url = f'{self.site_base}{url}'
        self.browser.get(full_url)
        time.sleep(3)

        source = self.browser.page_source

        soup = BeautifulSoup(source, 'html.parser')
        main = soup.find('div', {'class': 'kt-row'})

        targets = [
            '۴۰۶۰',
            '4060',
            '۳۰۷۰',
            '3070',
            '۴۰۷۰',
            '4070'
        ]

        for target in targets:
            if target in main.text:
                print('-' * 100)
                print(target)
                link = f'https://divar.ir{url}'
                print(f'    {link}')
                self.found.append(link)
                break
