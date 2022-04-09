import json
import time
import random
from typing import Union

from django.core.cache import cache
from django.conf import settings

from products.models import Product, ProductVariant
from products.robot.core.base_robot import RobotBase
from utils.logging import logger, plogger, plogger_flat, LOG_VALUE_WIDTH as LOG_W
from products.robot.urls import URLS
from products.robot.json_extraction import JSONExtractor
from products.robot.exceptions import StopRobot


def random_sleep(seconds: int = 1, gap: int = 1):
    time.sleep(round(random.uniform(seconds, seconds + gap), 2))


def check_stop_signal():
    if cache.get(settings.CACHE_KEY_STOP_ROBOT) == 'true':
        raise StopRobot()


class TrailingPriceRobot(RobotBase):
    """
    page_data: {
    'out_of_stock': list[dkpc]
    'variants_data': dict[dkpc: VarDataDict]
    }

    VarDataDict: {
    'has_competition': bool,
    'min_price': int,
    'my_price': int
    }
    """
    PRICE_GAP_THRESHOLD = 10000
    NO_COMPETITION_JUMP = 0.04

    data_extractor_class = JSONExtractor

    help = 'maintains price of our variants below competition price'

    def __init__(self, *args, **kwargs):
        self.dkp = kwargs.pop('dkp')
        super().__init__(*args, **kwargs)

    def run(self):
        check_stop_signal()
        logger('CYCLE START'.center(LOG_W), color='green')
        self.login()
        self.check_products()
        logger('CYCLE END'.center(LOG_W), color='green')
        self.report()

    def get_active_products(self):
        if self.dkp is not None and self.dkp.isdigit():
            return Product.objects.filter(dkp=self.dkp)
        else:
            return Product.objects.filter(is_active=True)

    def check_products(self):
        active_products = self.get_active_products()
        self.out_of_stock = []
        self.min_reached = []
        self.no_competition = []
        for product in active_products:
            check_stop_signal()
            logger(product.title, color='cyan')
            extractor = self.data_extractor_class(self.session, product)
            page_data = extractor.get_page_data()
            self.out_of_stock += page_data['out_of_stock']
            variants_data = page_data['variants_data']
            if variants_data:
                self.process_variants_data(variants_data)
            random_sleep(seconds=1)

    def process_variants_data(self, variants_data: dict):
        for dkpc, var_data in variants_data.items():
            check_stop_signal()
            if var_data['has_competition']:
                self.handle_competition(dkpc, var_data)
            else:
                self.no_competition.append(dkpc)
                self.set_no_competition_price(dkpc, var_data)
            random_sleep(seconds=3)

    def handle_competition(self, dkpc: int, var_data: dict):
        my_price = var_data['my_price']
        min_price = var_data['min_price']
        if my_price >= min_price:
            logger(f'{dkpc}: lower price exists'.center(LOG_W), color='yellow')
            self.adjust_price(dkpc, min_price)
        elif min_price - my_price >= self.PRICE_GAP_THRESHOLD:
            logger(f'{dkpc}: increasing price'.center(LOG_W), color='green')
            self.adjust_price(dkpc, min_price)

    def adjust_price(self, dkpc: int, competition_price: int):
        variant = ProductVariant.objects.select_related('product').get(dkpc=dkpc)
        new_price = competition_price - variant.actual_product.price_step
        if new_price < variant.price_min:
            logger(f'{dkpc}: minimum price reached'.center(LOG_W), color='red')
            self.min_reached.append(dkpc)
            return
        logger(f'{new_price = }')
        self.update_variant_price_rial(dkpc=dkpc, price=new_price)
        if not variant.has_competition:
            variant.has_competition = True
            variant.save()

    def set_no_competition_price(self, dkpc: int, var_data: dict):
        variant = ProductVariant.objects.get(dkpc=dkpc)
        if variant.has_competition:
            new_price = int(variant.price_min * (1 + self.NO_COMPETITION_JUMP))
            new_price -= new_price % 100  # round down to closest hundred
            if new_price > var_data['my_price']:
                logger(f'{dkpc}: no competition - increasing price', color='green')
                self.update_variant_price_rial(dkpc, new_price, increasing=True)
                variant.has_competition = False
                variant.save()

    def update_variant_price_rial(self, dkpc: Union[str, int], price: int, increasing: bool = False):
        digi_data = self.get_digi_variant_data(dkpc)
        payload = {
            'id':                        str(dkpc),
            'lead_time':                 digi_data['lead_time_latin'],
            'price_sale':                price,
            'marketplace_seller_stock':  digi_data['marketplace_seller_stock_latin'],
            'maximum_per_order':         '5',
            'oldSellerStock':            '5',
            'selling_chanel':            '',
            'is_buy_box_suggestion':     '0',
            'shipping_type':             'digikala',
            'seller_shipping_lead_time': '2',
        }
        response = self.session.post(URLS['update_product'], data=payload,
                                     headers={'user-agent': 'Mozilla/5.0'})
        logger(response)
        decoded = response.content.decode()
        data = json.loads(decoded)
        plogger(data)
        self.check_server_response_for_update(data, dkpc, price, increasing)

    def get_digi_variant_data(self, dkpc: int) -> dict:
        url = f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&sortOrder=desc&page=1&' \
              f'items=10&search[type]=product_variant_id&search[value]={dkpc}&'

        while True:
            res = self.session.get(url)
            try:
                response = res.json()
            except json.JSONDecodeError:
                logger('ERROR in json decode')
                logger(res.status_code)
                logger(res.content)
                if res.status_code == 429:
                    random_sleep(seconds=10)
                    continue
                else:
                    raise

            if response['status'] is True:
                digi_item = response['data']['items'][0]
                if not digi_item['product_variant_id'] == dkpc:
                    plogger({
                        'error':                            'different variant id from digikala search',
                        'our dkpc':                         dkpc,
                        'digikala item product_variant_id': digi_item['product_variant_id'],
                        'digikala item id':                 digi_item['id'],
                    }, color='red')
                    raise Exception('digikala search result dkpc is different from our variant dkpc!')
                return digi_item

            else:
                logger('ERROR in getting digi response')
                logger(res.status_code)
                logger(res.content)
                raise RuntimeError(f'ERROR in getting digi response for {dkpc = }')

    def check_server_response_for_update(self, response, dkpc, price, increasing):
        if not increasing:
            return
        price_range_error = 'قیمت فروش شما در بازه\u200cی قیمت مرجع نیست.'
        if response['status'] is False:
            if response['data']['price'] == price_range_error:
                new_price = price - 10000
                variant = ProductVariant.objects.get(dkpc=dkpc)
                if new_price > variant.price_min:
                    logger(f'new price: {new_price}')
                    random_sleep(seconds=3)
                    self.update_variant_price_rial(dkpc, new_price, increasing=True)
                else:
                    logger(f'can not increase price for: {dkpc} - price is already outside digi price span')
            else:
                raise Exception(f'could not update price of: {dkpc}')

    def report(self):
        logger(f'no competition: {len(self.no_competition)}'.center(LOG_W), color='green')
        logger(f'inactive: {len(self.out_of_stock)}'.center(LOG_W), color='red')
        self.iter_variants_for_report(self.out_of_stock)
        logger(f'minimum price reached: {len(self.min_reached)}'.center(LOG_W), color='yellow')

    @staticmethod
    def iter_variants_for_report(dkpc_list: list):
        for dkpc in dkpc_list:
            variant = ProductVariant.objects.get(dkpc=dkpc)
            plogger_flat({
                'title':    variant.product.title,
                'selector': variant.selector_values.first().value,
                'url':      f'https://www.digikala.com/product/dkp-{variant.product.dkp}'
            })
