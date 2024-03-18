import time
import json

from django.core.management import BaseCommand

import requests


def get_links(data):
    items = data['web_widgets']['post_list']
    links = []
    for item in items:
        payload = item['data']['action']['payload']
        token = payload['token']
        link = f'/v/blank/{token}'
        print(link)
        links.append(link)

    return links


def get_payload(page: int):
    return {
        "json_schema": {
            "brand_model": {
                "value": [
                    "Samand LX EF7-petrol"
                ]
            },
            "category":    {
                "value": "light"
            },
            "cities":      [
                "1"
            ],
            "sort":        {
                "value": "sort_date"
            }
        },
        # "last-post-date": 1703743376247506,
        "page":        page
    }


def send_request(page: int):
    url = 'https://api.divar.ir/v8/web-search/1/light'
    filters = get_payload(page)
    res = requests.post(url, json=filters)
    data = res.json()
    return get_links(data)


class Command(BaseCommand):

    def handle(self, *args, **options):
        page = 2
        all_links = []
        while True:
            print('-' * 100)
            print(f'{page = }')
            links = send_request(page)
            if len(links) == 0:
                break
            all_links.extend(links)
            time.sleep(2)
            page += 1

        all_links.reverse()
        print(all_links)
        with open('old_ads.json', 'w', encoding='utf-8') as f:
            json.dump(all_links, f)
