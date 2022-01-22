import time

from django.core.management import call_command

from celery import shared_task
from celery.utils.log import get_task_logger


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
