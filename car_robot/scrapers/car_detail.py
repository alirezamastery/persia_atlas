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
    'CarDetailScraper',
]


def random_sleep(seconds: int = 1, gap: int = 1):
    time.sleep(round(random.uniform(seconds, seconds + gap), 2))


xpath = {
    'title':       '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[1]/div[1]/div/div[1]',
    'time':        '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[1]/div[1]/div/div[2]',
    'kilometer':   '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[1]/div[4]/table/tbody/tr/td[1]',
    'year':        '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[1]/div[4]/table/tbody/tr/td[2]',
    'color':       '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[1]/div[4]/table/tbody/tr/td[3]',
    'description': '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[2]/div/div[2]/div/p',
}

info_map = {
    'نوع آگهی':            'ad_type',
    'برند و تیپ':          'model',
    'نوع سوخت':            'fuel',
    'وضعیت موتور':         'engine',
    'وضعیت شاسی‌ها':       'chassis',
    'شاسی جلو':            'chassis_front',
    'شاسی عقب':            'chassis_back',
    'وضعیت بدنه':          'body',
    'مهلت بیمهٔ شخص ثالث': 'insurance',
    'گیربکس':              'gearbox',
    'مایل به معاوضه':      'can_exchange',
    'قیمت پایه':           'price',
}

info_fields = [
    'ad_type',
    'model',
    'fuel',
    'engine',
    'chassis',
    'chassis_front',
    'chassis_back',
    'body',
    'insurance',
    'gearbox',
    'can_exchange',
    'price',
]

xpath_phone = {
    'show_phone_btn': '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[1]/div[2]/button[1]',
    'phone':          '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[1]/div[3]/div[1]/div/div[2]/a',
}

persia_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2NDQzOTc2LCJpYXQiOjE3MDM4NTE5NzYsImp0aSI6ImViMmE5NzEzNDA0NTQwYjU4OWYyMmMwOGM3NTMwNDFmIiwidXNlcl9pZCI6MX0.Wcg22IidzuCRfw0SVqtdD0ziA6eyVoDLtaRy9fYMgA0'
cookie_pickle_path = './car_robot/scrapers/divar.pkl'


class CarDetailScraper:

    def __init__(self, urls: list[str]):
        self.urls = urls
        firefox_options = FirefoxOptions()
        firefox_options.headless = False
        firefox_options.binary_location = settings.FIREFOX_BINARY
        self.table_rows = []
        service = Service(settings.GECKO_DRIVER_PATH)
        self.browser = Firefox(service=service, options=firefox_options)
        self.site_base = 'https://divar.ir'

    def run(self):
        logger('start')
        self.browser.get(self.site_base)
        cookies = pickle.load(open(cookie_pickle_path, 'rb'))
        for cookie in cookies:
            self.browser.add_cookie(cookie)

        for url in self.urls:
            self.extract_car_detail(url)

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
        time.sleep(5)

        source = self.browser.page_source
        with open('car_detail.html', 'w', encoding='utf-8') as f:
            f.write(source)

        for k, v in xpath.items():
            el = self.browser.find_element(By.XPATH, v)
            txt = el.text

            if k in ['kilometer', 'year']:
                val = unidecode(txt)
                val = val.replace(',', '')
                details[k] = int(val)
            elif k == 'time':
                parts = txt.split('،')
                details['time'] = parts[0].strip()
                details['location'] = parts[1].strip()
            else:
                details[k] = txt

        section_path = '/html/body/div[1]/div[2]/div/main/article/div/div[1]/section[1]'
        section_el = self.browser.find_element(By.XPATH, section_path)
        info_source = section_el.get_attribute('innerHTML')
        soup = BeautifulSoup(info_source, 'html.parser')
        divs = soup.find_all('div', recursive=False)
        container = divs[-1]
        rows = container.find_all('div', recursive=False)
        for row in rows:
            cells = row.find_all('div', recursive=False)
            key = cells[0].find('p', recursive=False).text
            model_field = info_map.get(key, None)
            if model_field is None:
                continue

            try:
                value = cells[1].find('p', recursive=False).text
            except:
                value = cells[1].find('a').text

            if model_field == 'price':
                value = value.split(' ')[0]
                value = unidecode(value)
                value = value.replace(',', '')
                value = int(value)

            details[model_field] = value

        for field in info_fields:
            if field not in details.keys():
                details[field] = ''

        try:
            phone_btn = self.browser.find_element(By.XPATH, xpath_phone['show_phone_btn'])
            phone_btn.click()
            time.sleep(6)
            phone_el = self.browser.find_element(By.XPATH, xpath_phone['phone'])
            details['phone'] = unidecode(phone_el.text)
        except:
            details['phone'] = 'مخفی'

        pprint(details)

        # headers = {
        #     'Authorization': f'Bearer {persia_token}'
        # }
        # persia_url = 'https://persia-atlas.com/api/car-robot/cars/'
        # res = requests.post(persia_url, json=details, headers=headers)
        # print(res.status_code)

        Car.objects.create(**details)

    def clean_up(self):
        logger('clean up')
        # pickle.dump(self.browser.get_cookies(), open('divar.pkl', 'wb'))
