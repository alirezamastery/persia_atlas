import time
import random
from typing import Union
from abc import ABC, abstractmethod

from .server import ServerSession
from utils.logging import logger, plogger


class RobotBase(ABC, ServerSession):
    ERROR_WAIT = 5

    @abstractmethod
    def run(self):
        """entry point to running the robot"""

    @staticmethod
    def loop_wait():
        time.sleep(round(random.uniform(1, 2), 2))

    def exception_wait(self):
        time.sleep(self.ERROR_WAIT)

    def update_variant_price_toman(self, dkpc: Union[str, int], price: int):
        url_update_product = 'https://seller.digikala.com/ajax/variants/inline/update/'
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
        response = self.session.post(url_update_product, data=payload,
                                     headers={'user-agent': 'Mozilla/5.0'})
        data = response.json()
        plogger(data)
        self.check_server_response_for_update(data, dkpc, price)

    def check_server_response_for_update(self, response, dkpc, price, increasing):
        price_range_error = 'قیمت فروش شما در بازه\u200cی قیمت مرجع نیست.'
        if response['status'] is False:
            if response['data']['price'] == price_range_error:
                new_price = price - 1000
                logger(f'new price: {new_price}')
                self.update_variant_price_toman(dkpc, new_price)
            else:
                raise Exception(f'could not update price of: {dkpc}')
