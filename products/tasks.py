import time

from django.core.management import call_command
from celery import shared_task
from celery.utils.log import get_task_logger

from products.models import ProductVariant
from utils.digi import variant_detail_request


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
def scrape_invoice_page(row_number: int):
    logger.info(f'starting to scrape invoice page, {row_number = }')
    call_command(f'scrape_invoice', f'--row={row_number}')


@shared_task()
def toggle_variants_status(
        actual_product_id: int,
        selector_ids: list,
        is_active: bool
):
    print(f'{actual_product_id = }')
    print(f'{is_active = }')
    dkpc_list = ProductVariant.objects \
        .filter(actual_product_id=actual_product_id, selector_id__in=selector_ids) \
        .values_list('dkpc', flat=True)
    print(f'{dkpc_list = }')

    if is_active is True:
        for dkpc in dkpc_list:
            variant_detail_request(dkpc, method='PUT', payload={'seller_stock': 3})
            time.sleep(0.2)

    for dkpc in dkpc_list:
        variant_detail_request(dkpc, method='PUT', payload={'is_active': is_active})
        time.sleep(0.2)

    variants = ProductVariant.objects.filter(dkpc__in=dkpc_list)
    for variant in variants:
        variant.is_active = False
    ProductVariant.objects.bulk_update(variants, fields=['is_active'])
