import json
import datetime as dt

import requests
from django.conf import settings
from rest_framework.exceptions import APIException

from utils.logging import plogger


def get_variant_search_url(dkpc):
    return f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&' \
           f'sortOrder=desc&page=1&items=10&search[type]=product_variant_id&search[value]={dkpc}&'


def get_variant_api_url(dkpc: int) -> str:
    return f'{settings.DIGIKALA_API_BASE_URL}/variants/{dkpc}/'


def send_digikala_api_request(url: str, *, method: str = 'GET', payload: dict = None) -> dict:
    try:
        res = requests.request(
            url=url,
            headers=settings.DIGIKALA_API_HEADERS,
            method=method,
            json=payload,
            timeout=5,
        )
    except requests.exceptions.RequestException:
        raise APIException('خطا در برقرار ارتباط با دیجیکالا')
    try:
        res_json = res.json()
    except json.decoder.JSONDecodeError:
        plogger(res.text)
        with open('err.html', 'w', encoding='utf-8') as f:
            f.write(f'--- {dt.datetime.now()} ---')
            f.write(res.text)
        raise APIException('پاسخ غیر عادی از دیجیکالا دریافت شد')
    if res_json['status'] == 'ok':
        return res_json['data']
    raise APIException(res_json)


def variant_detail_request(dkpc: int, *, method: str = 'GET', payload: dict = None) -> dict:
    url = get_variant_api_url(dkpc)
    return send_digikala_api_request(url=url, method=method, payload=payload)


def get_variant_list(query_params: dict) -> dict:
    url_query = ''
    for k, v in query_params.items():
        url_query += f'&{k}={v}'
    url = f'{settings.DIGIKALA_API_BASE_URL}/variants/?{url_query}'
    return send_digikala_api_request(url=url, method='GET')


def variant_detail_request_from_robot(
        dkpc: int,
        *,
        method: str = 'GET',
        payload: dict = None
) -> dict:
    url = get_variant_api_url(dkpc)
    try:
        res = requests.request(
            url=url,
            headers=settings.DIGIKALA_API_HEADERS,
            method=method,
            json=payload,
            timeout=5,
        )
    except requests.exceptions.RequestException:
        raise Exception('خطا در برقرار ارتباط با دیجیکالا')
    return res.json()


__all__ = [
    'get_variant_search_url',
    'get_variant_api_url',
    'variant_detail_request',
    'get_variant_list',
    'variant_detail_request_from_robot',
]
