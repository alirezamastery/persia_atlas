from django.conf import settings


def get_variant_search_url(dkpc):
    return f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&' \
           f'sortOrder=desc&page=1&items=10&search[type]=product_variant_id&search[value]={dkpc}&'


def get_variant_api_url(dkpc: int) -> str:
    return f'{settings.DIGIKALA_API_BASE_URL}{dkpc}/'


__all__ = [
    'get_variant_search_url',
    'get_variant_api_url',
]
