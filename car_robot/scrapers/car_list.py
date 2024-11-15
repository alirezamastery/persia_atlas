import time

from bs4 import BeautifulSoup
from django.conf import settings
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service

from utils.logging import logger


__all__ = [
    'CarListScraper',
]


class CarListScraper:

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
        container = soup.find('div', {'class': 'virtual-infinite-scroll__viewport'})
        wrapper = container.find('div', recursive=False)
        children = wrapper.find_all('div', recursive=False)

        links = []
        for child in children:
            link = child.find('a')
            href = link['href']
            print(href)
            links.append(href)

        return links
