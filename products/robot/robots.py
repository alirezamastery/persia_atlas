import json
import time
import random
from typing import Union

from products.models import Product, ProductVariant
from products.robot.core.base_robot import RobotBase
from utils.logging import logger, plogger, plogger_flat, LOG_VALUE_WIDTH as LOG_W
from .page import BuyBoxPage, CheckPricePage
from .urls import URLS


class TrailingPriceRobot(RobotBase):
    PRICE_LOWERING_STEP = 500
    PRICE_GAP_THRESHOLD = 1000
    NO_COMPETITION_JUMP = 0.05

    help = 'maintains price of our variants below competition price'

    def run(self):
        while True:
            logger('CYCLE START'.center(LOG_W), color='green')
            try:
                self.login()
                self.check_products()
                logger('CYCLE END'.center(LOG_W), color='green')
                self.report()
            except Exception as e:
                logger('ERROR:', e, color='red')
                self.exception_wait()
            else:
                break

    def check_products(self):
        active_products = Product.objects.filter(is_active=True)
        self.out_of_stock = []
        self.min_reached = []
        self.no_competition = []
        for product in active_products:
            logger(product.title, color='cyan')
            try:
                page = CheckPricePage(product)
            except json.decoder.JSONDecodeError:
                logger(f'ERROR: failed to load: {product.dkp}', color='red')
                continue
            page_data = page.get_page_data()
            self.out_of_stock += page_data['out_of_stock']
            variants_data = page_data['variants_data']
            # if variants_data:
            #     self.process_variants_data(variants_data)
            time.sleep(round(random.uniform(1, 2), 2))

    def process_variants_data(self, variants_data: dict):
        for dkpc, var_data in variants_data.items():
            while True:
                try:
                    if var_data['has_competition']:
                        self.handle_competition(dkpc, var_data)
                    else:
                        self.no_competition.append(dkpc)
                        self.set_no_competition_price(dkpc, var_data)
                    break
                except Exception as e:
                    logger('ERROR:', e, color='red')
                    self.exception_wait()

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
        new_price = competition_price - self.PRICE_LOWERING_STEP
        variant = ProductVariant.objects.get(dkpc=dkpc)
        if new_price < variant.price_min:
            logger(f'{dkpc}: minimum price reached'.center(LOG_W), color='red')
            self.min_reached.append(dkpc)
            return
        self.update_variant_price_toman(dkpc=str(dkpc), price=new_price)
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
                self.update_variant_price_toman(dkpc, new_price, increasing=True)
                variant.has_competition = False
                variant.save()

    def update_variant_price_toman(self, dkpc: Union[str, int], price: int, increasing: bool = False):
        payload = {
            'id':                        str(dkpc),
            'lead_time':                 '1',
            'price_sale':                price * 10,
            'marketplace_seller_stock':  '5',
            'maximum_per_order':         '2',
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

    def check_server_response_for_update(self, response, dkpc, price, increasing):
        if not increasing:
            return
        price_range_error = 'قیمت فروش شما در بازه\u200cی قیمت مرجع نیست.'
        if response['status'] is False:
            if response['data']['price'] == price_range_error:
                new_price = price - 1000
                logger(f'new price: {new_price}')
                self.update_variant_price_toman(dkpc, new_price, increasing=True)
            else:
                raise Exception(f'could not update price of: {dkpc}')

    def report(self):
        logger(f'no competition: {len(self.no_competition)}'.center(LOG_W), color='green')
        # self.iter_variants_for_report(self.no_competition)
        logger(f'inactive: {len(self.out_of_stock)}'.center(LOG_W), color='red')
        self.iter_variants_for_report(self.out_of_stock)
        logger(f'minimum price reached: {len(self.min_reached)}'.center(LOG_W), color='yellow')
        # self.iter_variants_for_report(self.min_reached)

    @staticmethod
    def iter_variants_for_report(dkpc_list: list):
        for dkpc in dkpc_list:
            variant = ProductVariant.objects.get(dkpc=dkpc)
            plogger_flat({
                'title':    variant.product.title,
                'selector': variant.selector_values.first().value,
                'url':      f'https://www.digikala.com/product/dkp-{variant.product.dkp}'
            })


class FindNotBuyBoxRobot(RobotBase):
    help = 'find variants that are not buy box'

    def run(self):
        self.check_products()
        self.report()

    def report(self):
        logger(f'not BUY BOX variants: {len(self.not_buy_box)}'.center(LOG_W), color='yellow')
        for variant in self.not_buy_box:
            plogger_flat({
                'title': variant.title,
                'color': COLORS[variant.color_code]["name"],
                'url':   f'https://www.digikala.com/product/dkp-{variant.product.dkp}'
            })

    def check_products(self):
        my_products = self.load_active_products()
        self.not_buy_box = []
        for dkp, my_variants in my_products.items():
            logger(my_variants[0].title)
            page = BuyBoxPage(dkp, my_variants)
            variants = page.get_all_variants()
            if variants:
                self.not_buy_box += page.find_not_buybox()
            else:
                logger('product does NOT have variant(s)!', color='red')
            self.loop_wait()


class UpdateMinPriceRobot(RobotBase):
    help = 'set price of variants to given amount'

    def run(self):
        self.login()
        self.set_prices()

    def set_prices(self):
        for dkp, my_variants in self.active_products.items():
            logger(my_variants[0].title)
            page = CheckPricePage(dkp, my_variants)
            page_data = page.get_page_data()
            variants_data = page_data['variants_data']
            if variants_data:
                self.process_variants_data(variants_data)
            time.sleep(round(random.uniform(1, 2), 2))

    def process_variants_data(self, variants_data: dict):
        for dkpc, var_data in variants_data.items():
            variant_obj = self.orm.get_by_dkpc(dkpc)
            while True:
                try:
                    if var_data['my_price'] < variant_obj.price_min:
                        logger(f'price of {dkpc} is lower than min', color='yellow')
                        self.update_variant_price_toman(dkpc, variant_obj.price_min)
                    break
                except Exception as e:
                    logger('ERROR:', e, color='red')
                    self.exception_wait()
