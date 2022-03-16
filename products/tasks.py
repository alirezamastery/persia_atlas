import time
import random

from django.core.management import call_command
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger
from products.models import *
from persia_atlas.digi import digi_session


logger = get_task_logger(__name__)


@shared_task
def add(x):
    logger.info(f'logger.info | the answer is: {x + 1}')
    print(f'print | the answer is: {x + 1}')
    with open('test.txt', 'w') as file:
        file.write('test task')
    return x + 1


@shared_task
def just_sleep():
    time.sleep(15)


@shared_task
def just_sleep_and_fail():
    time.sleep(5)
    raise Exception('some error')


@shared_task
def scrape_invoice_page():
    logger.info(f'starting to scrape invoice page')
    call_command('scrape_invoice')


@shared_task
def update_brand_status(brand_id: int, is_active: bool):
    variants = ProductVariant.objects.filter(actual_product__brand_id=brand_id)
    url = settings.DIGIKALA_URLS['update_variant_status']
    for variant in variants:
        logger.info(f'processing dkpc: {variant.dkpc}')
        payload = {
            'id':     variant.dkpc,
            'active': is_active
        }
        digikala_res = digi_session.post(url, payload)

        if digikala_res['status']:
            variant.is_active = is_active
            variant.save()
        else:
            logger.info(f'update of dkpc {variant.dkpc} failed from digikala')

        time.sleep(round(random.uniform(3, 4), 2))
