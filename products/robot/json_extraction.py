import requests
from requests.exceptions import RequestException

from ..models import Product, ProductVariant
from utils.logging import logger, plogger


class JSONExtractor:
    base_url = 'https://api.digikala.com/v1/product/'

    def __init__(self, product: Product):
        self.product = product
        self.selector_type = self.product.type.selector_type
        self.my_variants = list(self.product.variants.filter(is_active=True))
        self.others_variants = None
        self.page_variants = None
        self.out_of_stock = []

        page_url = f'https://www.digikala.com/product/dkp-{self.product.dkp}'
        logger(page_url, color='cyan')

        url = self.get_product_url()
        try:
            self.data = requests.get(url, timeout=5).json()
        except RequestException as e:
            raise e
        except Exception as e:
            logger('ERROR in getting product json data:', e, color='red')

    def get_product_url(self):
        return f'{self.base_url}{self.product.dkp}/'

    def get_page_data(self) -> dict:
        self.get_variants_data()
        if self.page_variants is None:
            logger('product does NOT have any variants in its page!', color='red')
            return {
                'out_of_stock':  [var.dkpc for var in self.my_variants],
                'variants_data': None
            }

        variants_data = {}
        for var in self.my_variants:
            logger(f'dkpc: {var.dkpc} |'
                   f' selector: {self.selector_type.title} - value: {var.selector.value} - {var.selector.digikala_id}')
            my_price = self.get_variant_price(int(var.dkpc))
            logger(f'{my_price = }')
            if my_price > 0:
                variants_data[var.dkpc] = self.check_variant_competition(var)
                variants_data[var.dkpc]['my_price'] = my_price
            else:
                self.out_of_stock.append(var.dkpc)
        return {
            'out_of_stock':  self.out_of_stock,
            'variants_data': variants_data
        }

    def get_variants_data(self):
        """
        find variants that have the same color or size as my variant.
        """

        my_variants_selector_ids = [v.selector.digikala_id for v in self.my_variants]
        my_variants_dkpcs = [int(v.dkpc) for v in self.my_variants]
        logger(f'{my_variants_selector_ids = }')
        logger(f'{my_variants_dkpcs = }')

        try:
            variants = self.data['data']['product'].get('variants')
            if variants is None or len(variants) == 0:
                return
        except Exception as e:
            logger('error in getting variants data:', e, color='red')
            return

        self.page_variants = variants
        others_variants = {selector: [] for selector in my_variants_selector_ids}
        selector_title = self.selector_type.title
        logger(f'{selector_title = }')
        for var_data in variants:
            dkpc = var_data['id']
            # right now variants in page only have either color or size and we have only
            # 'size' and 'color' in our database for ProductTypeSelector table
            var_selector_obj = var_data.get(self.selector_type.title)
            if var_selector_obj is None:
                raise Exception(f'found a variant that does not have selector data: {dkpc}')
            selector_id = var_selector_obj['id']
            if selector_id in my_variants_selector_ids and dkpc not in my_variants_dkpcs:
                others_variants[selector_id].append(dkpc)
        plogger(others_variants, color='yellow')
        self.others_variants = others_variants

    def get_variant_price(self, variant_id: int) -> int:
        for var in self.page_variants:
            if var['id'] == variant_id:
                return var['price']['selling_price']
        return -1

    def check_variant_competition(self, my_var: ProductVariant) -> dict:
        var_info = {'has_competition': False, 'min_price': None}
        other_variant_ids = self.others_variants[my_var.selector.digikala_id]
        if len(other_variant_ids) > 0:
            var_info['has_competition'] = True
            other_prices = self.get_other_prices(other_variant_ids)
            var_info['min_price'] = min(other_prices)
        return var_info

    def get_other_prices(self, other_variant_ids: list) -> list:
        other_prices = []
        for var_id in other_variant_ids:
            price = self.get_variant_price(var_id)
            other_prices.append(price)
        return other_prices
