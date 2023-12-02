import time
import datetime as dt
from zoneinfo import ZoneInfo

import requests
from django.core.management import BaseCommand
from khayyam import JalaliDate, JalaliDatetime

from accounting.models import *
from utils.logging import get_tehran_datetime


def get_url(invoice: int, page: int):
    return f'https://seller.digikala.com/api/v2/invoices/{invoice}/items/22/category_based?page={page}&size=100'


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--invoice',
            type=int,
        )
        parser.add_argument(
            '--cookies',
            type=str,
        )

    def handle(self, *args, **options):
        invoice_num = options.get('invoice')
        cookie_str = options.get('cookies')

        page = 1
        url = get_url(invoice_num, page)

        cookie_pairs = cookie_str.split(';')
        cookie_pairs = [p.split('=') for p in cookie_pairs]
        cookies = {p[0]: p[1] for p in cookie_pairs}

        res = requests.get(url, cookies=cookies)

        if res.status_code != 200:
            with open('invoice_from_api_errors.txt', 'a', encoding='utf-8') as log_file:
                date = get_tehran_datetime()
                log_file.write(f'STATUS CODE != 200: {date:-^100}\n')
                log_file.write(res.json())
                log_file.write('\n' * 2)
                return

        data = res.json()['data']
        rows = data['items']

        # Invoice date:
        meta_data = data['meta_data']
        start_date = dt.datetime.strptime(meta_data['from_date']['date'], '%Y-%m-%d %H:%M:%S.%f')
        end_date = dt.datetime.strptime(meta_data['to_date']['date'], '%Y-%m-%d %H:%M:%S.%f')
        start_date_persian = JalaliDate(start_date).strftime('%Y/%m/%d')
        end_date_persian = JalaliDate(end_date).strftime('%Y/%m/%d')
        print(start_date, start_date_persian)
        print(end_date, end_date_persian)

        try:
            invoice = Invoice.objects.get(number=invoice_num)
            invoice.invoice_items.all().delete()
        except Invoice.DoesNotExist:
            invoice = Invoice.objects.create(
                number=invoice_num,
                start_date_persian=start_date_persian,
                end_date_persian=end_date_persian,
                start_date=start_date,
                end_date=end_date
            )

        # Get other pages if exist:
        pager = data['pager']
        total_pages = pager['total_pages']
        if total_pages > 1:
            while page < total_pages:
                page += 1
                time.sleep(1)

                url = get_url(invoice_num, page)
                res = requests.get(url=url, cookies=cookies)
                data = res.json()['data']
                rows = [*rows, *data['items']]

        for i, row in enumerate(rows, start=1):
            print(i, row)
            event_date = row['event_datetime']
            date_naive = dt.datetime.strptime(event_date['date'], '%Y-%m-%d %H:%M:%S.%f')
            date_aware = date_naive.astimezone(tz=ZoneInfo(event_date['timezone']))
            date_persian = JalaliDatetime(date_aware).strftime('%Y/%m/%d %H:%M')
            InvoiceItem.objects.create(
                invoice=invoice,
                row_number=i,
                code=row['id'],
                date=date_aware,
                date_persian=date_persian,
                dkpc=row['variant_code'].replace('DKPC-', ''),
                variant_title=row['variant_title'].strip().replace(',', '').replace(u'\u200c', ''),
                order_id=row['order_id'],
                serial=row['item_serial'],
                credit=row['credit'],
                debit=row['debit'],
                credit_discount=row['general_discount_credit'],
                debit_discount=row['general_discount_debit'],
                credit_final=row['final_credit'],
                debit_final=row['final_debit'],
                description=row['description'],
            )

    sample_row = {
        'id':                      2929365070,
        'event_datetime':          {
            'date':          '2023-07-23 08:00:25.000000',
            'timezone_type': 3,
            'timezone':      'Asia/Tehran'
        },
        'variant_code':            'DKPC-22623441',
        'variant_title':           'جعبه ابزار مهر مدل Me16i | نارنجی کم\u200cرنگ | گارانتی اصالت و سلامت فیزیکی کالا',
        'order_id':                207487036,
        'item_serial':             '2EB56179',
        'credit':                  0,
        'debit':                   147200,
        'general_discount_credit': 0,
        'general_discount_debit':  0,
        'final_credit':            0,
        'final_debit':             147200,
        'description':             'کمیسیون فروش با درصد 8 برای فروش به مبلغ 1,840,000',
        'calculation_model_type':  'category_based'
    }
