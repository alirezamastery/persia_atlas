import json

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

from products.models import Product , ProductVariant
from utils.logging import logger, plogger, LOG_VALUE_WIDTH, plogger_flat


class PageBase:
    """Base structure for parsing product page data"""

    def __init__(self, product_obj: Product):
        self.product_obj = product_obj
        self.my_variants = list(self.product_obj.variants.all())

        # so far we have only seen one variant selector in each product page
        # so we don't add more than more than one selector to ProductType objects
        # hence the .first()
        self.selector = self.product_obj.type.selectors.first()

        page_html = self.get_product_page(product_obj.dkp)
        self.soup = BeautifulSoup(page_html, 'html.parser')
        self.suppliers_div = self.soup.find('div', class_='c-table-suppliers__body')

    @staticmethod
    def get_product_page(dkp):
        url = f'https://www.digikala.com/product/dkp-{dkp}'
        logger(url, color='cyan')
        response = requests.get(url, timeout=5, headers={'user-agent': 'Mozilla/5.0'})
        return response.content

    def find_other_sellers_variants(self):
        """
        find variants that have the same color or size as my variant.
        variants data is in a javascript variable called 'ecpd2'
        """

        my_variants_selectors = [v.selector_values.first().digikala_id for v in self.my_variants]
        my_variants_dkpcs = [v.dkpc for v in self.my_variants]
        logger(f'{my_variants_selectors = }')
        logger(f'{my_variants_dkpcs = }')

        ecpd2 = self.extract_javascript_object('ecpd2')
        variants_js = ecpd2.get('variants')
        if variants_js is None:
            return None

        other_variants = {selector: [] for selector in my_variants_selectors}

        for var_data in variants_js:
            # right now variants in page only have either color or size and we have only
            # 'size' and 'color' in our database for ProductTypeSelector table
            if var_data[self.selector.title] in my_variants_selectors and \
                    str(var_data['id']) not in my_variants_dkpcs:
                other_variants[var_data['color']].append(var_data['id'])

        return other_variants

    def extract_javascript_object(self, obj_name: str):
        scripts = self.soup.findAll('script')
        scripts = [script.string for script in scripts if script.string is not None]
        script = ' '.join(scripts)
        var = script.split(f'var {obj_name} = ', 1)[-1].split(';', 1)[0]
        return json.loads(var)

    def get_all_variants(self):
        try:
            self.other_variants = self.find_other_sellers_variants()
            if self.other_variants is None:
                return None
        except Exception as e:
            logger('ERROR:', e, color='red')
            return None
        return self.soup.find('ul', class_='js-product-variants')


class CheckPricePage(PageBase):

    def get_page_data(self) -> dict:
        all_variants = self.get_all_variants()
        if all_variants is None:
            logger('product does NOT have any variants in its page!', color='red')
            return {
                'out_of_stock':  self.my_variants,
                'variants_data': None
            }
        self.out_of_stock = []
        variants_data = {}
        for var in self.my_variants:
            # clr = var.color_code
            # if self.product_obj.type.selectors.first().title == 'color':
            #     clr = var.selector_values.first().value
            # else:
            #     clr = 'white'
            logger(f'selector: {self.selector.title} - value: {var.selector_values.first().value} - '
                   f'{var.selector_values.first().digikala_id}')
            my_price = self.get_variant_price(var.dkpc)
            if my_price > 0:
                variants_data[var.dkpc] = self.check_variant_competition(var)
                variants_data[var.dkpc]['my_price'] = my_price
            else:
                self.out_of_stock.append(var.dkpc)
        return {
            'out_of_stock':  self.out_of_stock,
            'variants_data': variants_data
        }

    def check_variant_competition(self, my_var: ProductVariant) -> dict:
        var_info = {'has_competition': False, 'min_price': None}
        other_variant_ids = self.other_variants[my_var.selector_values.first().digikala_id]
        if len(other_variant_ids) > 0:
            var_info['has_competition'] = True
            other_prices = self.get_other_prices(other_variant_ids)
            var_info['min_price'] = min(other_prices)
        return var_info

    def get_other_prices(self, other_variant_ids: list) -> list:
        if len(other_variant_ids) == 0:
            raise Exception('list of other_variant_ids is empty')
        other_prices = []
        for other_variant_id in other_variant_ids:
            price = self.get_variant_price(other_variant_id)
            other_prices.append(price)
        return other_prices

    def get_variant_price(self, variant_id: int) -> int:
        supplier_div = self.suppliers_div.find('div', {'data-variant': variant_id})
        if supplier_div is None:
            logger(f'{variant_id}: not found in the page'.center(LOG_VALUE_WIDTH), color='magenta')
            return -1
        price = self.find_supplier_price(supplier_div)
        supplier_name = supplier_div.find('p', {'class': 'c-table-suppliers__seller-name'})
        supplier_name = supplier_name.find('a').text.strip()
        logger(f'{variant_id:<10}: {price:<9,} | {supplier_name} |')
        return price

    @staticmethod
    def find_supplier_price(supplier_div) -> int:
        price_element = supplier_div.find('div', class_='c-price__value js-seller-section-price')
        price_text = price_element.text.strip().replace(',', '')
        price_str = unidecode(price_text)  # persian to english
        return int(price_str)


class BuyBoxPage(PageBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.not_buy_box = []

    def find_not_buybox(self):
        for my_variant in self.my_variants:
            self.check_variant_buybox(my_variant)
        return self.not_buy_box

    def check_variant_buybox(self, my_var):
        logger(f'check color code: {my_var.color_code}', color=COLORS[my_var.color_code]['hex'])
        other_variant_ids = self.other_variants[my_var.color_code]
        if my_var.is_active and len(other_variant_ids) > 0:
            index_map = self.variant_div_index_map(my_var, other_variant_ids)
            if index_map is None:
                return
            min_index = min(index_map.keys())
            if index_map[min_index] != str(my_var.dkpc):
                self.not_buy_box.append(my_var)

    def variant_div_index_map(self, my_variant, other_variant_ids):
        """
        get index of each variant div in suppliers_div
        the smallest index is the BUY BOX in that color code (as far as I know)
        """
        all_rows = self.suppliers_div.find_all('div', class_='c-table-suppliers__row')
        index_map = {}
        my_variant_row = self.suppliers_div.find('div', {'data-variant': my_variant.dkpc})
        if my_variant_row is None:
            return None
        index_map[all_rows.index(my_variant_row)] = my_variant_row['data-variant']
        for other_var in other_variant_ids:
            other_var_row = self.suppliers_div.find('div', {'data-variant': other_var})
            index_map[all_rows.index(other_var_row)] = other_var_row['data-variant']
        return index_map
