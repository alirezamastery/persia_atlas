import time
from pprint import pp
import datetime as dt
from zoneinfo import ZoneInfo

import requests
from django.core.management import BaseCommand
from khayyam import JalaliDate, JalaliDatetime

from accounting.models import *
from utils.logging import get_tehran_datetime


def get_url(invoice: int, page: int):
    return f'https://seller.digikala.com/api/v2/invoices/{invoice}/items/22/category_based?page={page}&size=100'


cookie_str = '_sp_id.13cb=a20af8e7-92e0-49e7-b2ef-aba18811c7e6.1651909389.357.1711450350.1711441136.6d16bd74-b4ff-4cd6-bf40-4962733a4d96..5b835e14-2e46-475d-a06b-d66ee98fa2e2.1711450001666.4; tracker_glob_new=bXSlSoT; _ga_4S04WR965Q=GS1.1.1684848413.21.0.1684848420.0.0.0; _ga=GA1.1.631735578.1676385344; _ga_LR50FG4ELJ=GS1.1.1694277899.71.1.1694278211.60.0.0; _sp_id.3a05=193fc901-a20b-4e2a-9fea-8d665c9702cc.1694169442.2.1694447054.1694169442.a0c4b6fc-ae13-4b68-be1a-40281d938ba0.4411646a-076f-44d5-b62d-23cdeb23b3c4.c6df72b2-85e3-439a-b9b6-c71455b96195.1694447053583.1; _ga_YTPKDQLPZM=GS1.1.1694447056.1.0.1694447056.0.0.0; _ga_50CEWK5GC9=GS1.1.1696782005.30.0.1696782005.0.0.0; _ga_QQKVTD5TG8=GS1.1.1711447208.53.1.1711449766.0.0.0; Digikala:User:Token:new=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo3NDI1MjQsImV4cGlyZV90aW1lIjoxNzEyMTUzNDE1LCJwYXlsb2FkIjpbXSwicGFzc3dvcmRfdmVyc2lvbiI6MiwidHlwZSI6InRva2VuIn0.t-g9mqB4WLg42n_tRa84zscWII38aUB3F71F5iqFC7U; ab_test_experiments=%5B%228b29e3376be23005993b066a7741e54e%22%2C%22229ea1a233356b114984cf9fa2ecd3ff%22%5D; TS01b6ea4d=0102310591122dc978103696ef16b14dfb6271a4d54fd76eb7daaaeebcf1b04734d5fd5d6a0f82da0936dedd5eadad42f177c80e226829550d788d289930aa1fa8eb08daf9ffb98a07b5bddf745152c25b1d89bb5f; PHPSESSID=sf0b54icue858bahiatl1osipt; TS018d011a=01023105910235874dff603309442d0a385a9ef253899e1acc651c1eea0923369d673d4eeaef830367621554fe1d1550216b68d14acb8fc4fb5d09ae72d416549d3872ff3f51c27b959870e43800e293752973e222; _sp_ses.13cb=*; tracker_session=7t6QfCO; seller_api_access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJ0b2tlbl9pZCI6MTQyMjAwOTYsInNlbGxlcl9pZCI6NzQwMDM3LCJwYXlsb2FkIjp7InVzZXJuYW1lIjoicGVyc2lhLmF0bGFzY29AZ21haWwuY29tIiwicmVnaXN0ZXJfcGhvbmUiOiI5ODkzNTMwNjM1MzYiLCJlbWFpbCI6InBlcnNpYS5hdGxhc2NvQGdtYWlsLmNvbSIsImJ1c2luZXNzX25hbWUiOiJcdTA2N2VcdTA2MzFcdTA2MzRcdTA2Y2NcdTA2MjcgXHUwNjI3XHUwNjM3XHUwNjQ0XHUwNjMzIiwiZmlyc3RfbmFtZSI6Ilx1MDYzM1x1MDYzOVx1MDY0YVx1MDYyZiIsImxhc3RfbmFtZSI6Ilx1MDYyZlx1MDYzNFx1MDYyYVx1MDY0YSBcdTA2MmVcdTA2NDhcdTA2NGFcdTA2MmZcdTA2NDNcdTA2NGEiLCJjb21wYW55X25hbWUiOm51bGwsInZlcmlmaWVkX2J5X290cCI6WyJwZXJzaWEuYXRsYXNjb0BnbWFpbC5jb20iXX0sImV4cCI6MTcxMjMxMzAyNn0.RlZgLRJmF6_Md8C2tuLfRvHGtb2TfbjYLB72H3t82SliaDikq25_gMvjPwgKCKyP; seller_api_otp_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJ0eXBlIjoib3RwIiwidG9rZW5faWQiOjE0MjIwMDk1LCJzZWxsZXJfaWQiOm51bGwsInZlcmlmaWVkX2J5X290cCI6InBlcnNpYS5hdGxhc2NvQGdtYWlsLmNvbSIsImV4cCI6MTcxMjMxMzAyNn0.JGs9LorrZYRGFlu76_mLpDXSdLeXTrtFUUwKT0EzvVNVGK1k05kGVncsy76bzjWY'


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--invoice',
            type=int,
        )

    def handle(self, *args, **options):
        invoice_num = options.get('invoice')

        page = 1
        url = get_url(invoice_num, page)

        cookie_pairs = cookie_str.split(';')
        cookie_pairs = [p.split('=') for p in cookie_pairs]
        cookies = {p[0].strip(): p[1].strip() for p in cookie_pairs}
        pp(cookies)

        res = requests.get(url, cookies=cookies)

        if res.status_code != 200:
            pp(res.json())
            return
            # with open('invoice_from_api_errors.txt', 'a', encoding='utf-8') as log_file:
            #     date = get_tehran_datetime()
            #     log_file.write(f'STATUS CODE != 200: {date:-^100}\n')
            #     log_file.write(res.json())
            #     log_file.write('\n' * 2)
            #     return

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
            print(i, '-' * 100)
            pp(row)
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
