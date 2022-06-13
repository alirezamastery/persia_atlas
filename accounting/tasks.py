from django.core.management import call_command

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def scrape_invoice_page():
    logger.info(f'starting to scrape invoice page')
    call_command('scrape_invoice')
