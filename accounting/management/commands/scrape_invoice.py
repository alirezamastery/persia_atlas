import time
import random
from typing import Optional
from zoneinfo import ZoneInfo
from pprint import pprint

from bs4 import BeautifulSoup
from unidecode import unidecode
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from django.core.management import BaseCommand
from django.conf import settings
from khayyam import JalaliDate, JalaliDatetime

from accounting.models import Invoice, InvoiceItem
from utils.logging import logger
from utils.json_db import JsonDB


COLUMNS_INDEX_MAP = {
    0:  'row_number',
    1:  'code',
    2:  'date_persian',
    3:  'dkpc',
    4:  'variant_title',
    5:  'order_id',
    6:  'serial',
    7:  'credit',
    8:  'debit',
    9:  'credit_discount',
    10: 'debit_discount',
    11: 'credit_final',
    12: 'debit_final',
    13: 'description',
    14: 'calculated',
}

GECKO_DRIVER_PATH = settings.GECKO_DRIVER_PATH

LOGIN_URL = 'https://seller.digikala.com/account/login/?_back=https://seller.digikala.com/'
DIGI_URLS = {
    'login':        'https://seller.digikala.com/account/login/?_back=https://seller.digikala.com/',
    'invoice_list': 'https://seller.digikala.com/sellerinvoice/',
}
LOGIN_CREDENTIALS = {
    'login[email]':    'saeeddash94@gmail.com',
    'login[password]': 'Power$1400',
    # 'remember':        True
}

XPATH_USERNAME = '/html/body/div[1]/main/div/form/div[1]/div/div/input'
XPATH_PASSWORD = '/html/body/div[1]/main/div/form/div[2]/div/div/input'


class ScrapeInvoicePageNoDB:

    def __init__(self, invoice_row_index: int):
        self.invoice_row_index = invoice_row_index
        firefox_options = FirefoxOptions()
        firefox_options.headless = True
        self.table_rows = []
        service = Service(GECKO_DRIVER_PATH)
        self.browser = Firefox(service=service, options=firefox_options)

    def clean_up(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        db = JsonDB()
        username = db.get('digi_username')
        password = db.get('digi_password')
        creds = {
            'login[email]':    username,
            'login[password]': password
        }
        self.browser.get(LOGIN_URL)
        username_btn = self.browser.find_element(By.XPATH, XPATH_USERNAME)
        password_btn = self.browser.find_element(By.XPATH, XPATH_PASSWORD)
        username_btn.send_keys(creds['login[email]'])
        password_btn.send_keys(creds['login[password]'])
        submit_btn = self.browser.find_element(By.ID, 'btnSubmit')
        submit_btn.click()

    @staticmethod
    def random_sleep(base: int, span: int):
        time.sleep(round(random.uniform(base - span, base + span), 2))

    def run(self):
        logger('login attempt')
        self.login()
        logger('login complete')
        self.go_to_invoices()
        self.go_to_invoice_items()
        self.save_invoice()
        while True:
            self.extract_table_data()
            pagination_rows = self.get_pagination_row()
            if pagination_rows is None or (isinstance(pagination_rows, list) and len(pagination_rows) == 0):
                break
            is_last_page, pagination_btns = self.check_pagination_btns(pagination_rows)
            if is_last_page:
                break
            next_page = pagination_btns[-2].find_element(By.TAG_NAME, 'a')
            next_page.click()
            self.random_sleep(4, 2)
        pprint(self.table_rows)
        self.save_invoice_items()

    def go_to_invoices(self):
        self.browser.get(DIGI_URLS['invoice_list'])
        time.sleep(2)
        table = self.browser.find_element(By.TAG_NAME, 'table')
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        tr = tbody.find_elements(By.TAG_NAME, 'tr')[self.invoice_row_index]
        td = tr.find_elements(By.TAG_NAME, 'td')[13]
        link = td.find_element(By.TAG_NAME, 'a')
        href = link.get_attribute('href')
        logger(f'{href = }')
        self.invoice_number = int(link.get_attribute('data-invoice-id'))
        logger('invoice number:', self.invoice_number)
        link.click()
        time.sleep(2)

    def go_to_invoice_items(self):
        table = self.browser.find_element(By.TAG_NAME, 'table')
        link = table.find_element(By.TAG_NAME, 'a')
        href = link.get_attribute('href')
        logger(f'{href = }')
        link.click()
        time.sleep(2)

    def save_invoice(self):
        start_date_persian = self.browser.find_element(By.XPATH, '//input[@name="startDate"]').get_attribute('value')
        end_date_persian = self.browser.find_element(By.XPATH, '//input[@name="endDate"]').get_attribute('value')
        start_date_persian = unidecode(start_date_persian)
        end_date_persian = unidecode(end_date_persian)
        logger(f'{start_date_persian = }')
        logger(f'{end_date_persian = }')
        try:
            self.invoice = Invoice.objects.get(number=self.invoice_number)
            logger('this invoice is already in the database', color='yellow')
            logger(f'invoice object: {self.invoice}')
            self.invoice.invoice_items.all().delete()
        except Invoice.DoesNotExist:
            logger('saving new invoice in database', color='green')
            start_date = JalaliDate.strptime(start_date_persian, '%Y/%m/%d').todate()
            end_date = JalaliDate.strptime(end_date_persian, '%Y/%m/%d').todate()
            logger(f'{start_date = }')
            logger(f'{end_date = }')
            self.invoice = Invoice.objects.create(
                number=self.invoice_number,
                start_date_persian=start_date_persian,
                end_date_persian=end_date_persian,
                start_date=start_date,
                end_date=end_date
            )

    def get_pagination_row(self) -> Optional[list[WebElement]]:
        try:
            return self.browser.find_elements(By.CLASS_NAME, 'uk-pagination')
        except NoSuchElementException:
            return None

    @staticmethod
    def check_pagination_btns(pagination_rows: list[WebElement]):
        upper_pagination_row = pagination_rows[0]
        pagination_btns = upper_pagination_row.find_elements(By.TAG_NAME, 'li')
        active_btn = upper_pagination_row.find_element(By.CLASS_NAME, 'uk-active')
        logger(active_btn.text)
        logger(f'active btn index = {pagination_btns.index(active_btn)}')
        btn_index_neg = pagination_btns.index(active_btn) - len(pagination_btns)
        logger(f'{btn_index_neg = }')
        return btn_index_neg == -3, pagination_btns

    def extract_table_data(self):
        source = self.browser.page_source
        page = BeautifulSoup(source, 'html.parser')
        tbody = page.find('tbody')
        logger(f'{len(tbody) = }')
        rows = tbody.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            row_data = {}
            for i, cell in enumerate(cells):
                txt = cell.text.strip().replace(',', '').replace(u'\u200c', '')
                if i in [0, 2, 7, 8, 9, 10, 11, 12]:  # columns with persian numbers
                    txt = unidecode(txt)
                if i == 3:
                    txt = txt.replace('DKPC-', '')
                row_data[COLUMNS_INDEX_MAP[i]] = txt
            date_naive = JalaliDatetime.strptime(row_data['date_persian'], '%Y/%m/%d %H:%M').todatetime()
            date_aware = date_naive.astimezone(tz=ZoneInfo('Asia/Tehran'))
            row_data['date'] = date_aware
            self.table_rows.append(row_data)

    def save_invoice_items(self):
        for row in self.table_rows:
            InvoiceItem.objects.create(**row, invoice=self.invoice)


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--row',
            type=int,
            default=1,
        )

    def handle(self, *args, **options):
        row = options.get('row')
        if row < 1:
            raise Exception('row number should be greater than 0')
        row_index = row - 1

        robot = ScrapeInvoicePageNoDB(row_index)
        try:
            robot.run()
        except Exception as e:
            logger('scraping error', e, color='red')
        finally:
            robot.clean_up()
