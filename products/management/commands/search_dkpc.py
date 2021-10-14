import requests
from django.core.management import BaseCommand
from django.conf import settings
from products.robot.robots import TrailingPriceRobot
from utils.logging import logger, plogger


class Command(BaseCommand):

    def handle(self, *args, **options):
        session = requests.Session()
        response = session.post(settings.DIGIKALA_LOGIN_URL,
                                data=settings.DIGIKALA_LOGIN_CREDENTIALS,
                                timeout=30)
        logger(response, color='yellow')
        logger(f'{response.url = }', color='yellow')
        if response.url == settings.DIGIKALA_LOGIN_URL:
            raise Exception('could not login')
        dkpc = 22623942
        url = f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&sortOrder=desc&page=1&' \
              f'items=10&search[type]=product_variant_id&search[value]={dkpc}&'
        res = session.get(url)
        res = res.json()
        if res['status']:
            plogger(res['data'])
            digi_item = res['data']['items'][0]
            if digi_item['product_variant_id'] == dkpc:
                print('OK OK')
