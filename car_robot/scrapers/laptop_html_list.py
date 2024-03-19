import time
import re
import random
from typing import Optional
from zoneinfo import ZoneInfo
from pprint import pprint

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from django.core.management import BaseCommand
from django.conf import settings

from utils.logging import logger


__all__ = [
    'LaptopFirstPageListScraper',
]


class LaptopFirstPageListScraper:

    def __init__(self, url: str):
        self.url = url
        firefox_options = FirefoxOptions()
        firefox_options.headless = False
        firefox_options.binary_location = settings.FIREFOX_BINARY
        self.table_rows = []
        service = Service(settings.GECKO_DRIVER_PATH)
        self.browser = Firefox(service=service, options=firefox_options)

    def run(self):
        logger('start')
        self.browser.get(self.url)
        time.sleep(4)

        source = self.browser.page_source
        with open('temp.html', 'w', encoding='utf-8') as f:
            f.write(source)
        soup = BeautifulSoup(source, 'html.parser')
        container = soup.find_all('div', attrs={'class': re.compile('^post-list__widget-col*')})

        links = []
        for el in container:
            link = el.find('a')
            href = link['href']
            print(href)
            links.append(href)

        return links
