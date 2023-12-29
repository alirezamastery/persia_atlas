import pickle

from django.core.management import BaseCommand
from django.conf import settings
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service


DETAIL_URL = 'https://divar.ir/v/%D8%B3%D9%85%D9%86%D8%AF-lx-ef7-%D8%A8%D9%86%D8%B2%DB%8C%D9%86%DB%8C-%D9%85%D8%AF%D9%84-%DB%B1%DB%B3%DB%B9%DB%B6/QZGysoIO'
cookie_pickle_path = './car_robot/scrapers/divar.pkl'


class CookiePickler:

    def __init__(self, url: str):
        self.url = url
        firefox_options = FirefoxOptions()
        firefox_options.headless = False
        firefox_options.binary_location = settings.FIREFOX_BINARY
        self.table_rows = []
        service = Service(settings.GECKO_DRIVER_PATH)
        self.browser = Firefox(service=service, options=firefox_options)

    def run(self):
        self.browser.get(self.url)

        input('Login with your mobile and press enter...')

        pickle.dump(self.browser.get_cookies(), open(cookie_pickle_path, 'wb'))

        self.browser.quit()


class Command(BaseCommand):

    def handle(self, *args, **options):
        robot = CookiePickler(DETAIL_URL)
        robot.run()
