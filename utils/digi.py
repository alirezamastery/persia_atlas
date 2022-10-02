import json

import requests
from django.conf import settings
from rest_framework.exceptions import APIException

from utils.logging import plogger


def get_variant_search_url(dkpc):
    return f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&' \
           f'sortOrder=desc&page=1&items=10&search[type]=product_variant_id&search[value]={dkpc}&'


def get_variant_api_url(dkpc: int) -> str:
    return f'{settings.DIGIKALA_API_BASE_URL}variants/{dkpc}/'


def get_variant_detail(dkpc: int) -> dict:
    url = get_variant_api_url(dkpc)
    try:
        res = requests.get(url, headers=settings.DIGIKALA_API_HEADERS)
    except requests.exceptions.RequestException:
        raise APIException('خطا در برقرار ارتباط با دیجیکالا')
    try:
        res_json = res.json()
    except json.decoder.JSONDecodeError:
        raise APIException('پاسخ غیر عادی از دیجیکالا دریافت شد')
    plogger(res_json)
    if res_json['status'] == 'ok':
        return res_json['data']
    raise APIException(f'digikala response: {res_json["message"]}')


__all__ = [
    'get_variant_search_url',
    'get_variant_api_url',
    'get_variant_detail',
]
