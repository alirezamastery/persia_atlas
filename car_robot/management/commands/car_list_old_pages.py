import time
import json
from pprint import pprint

from django.core.management import BaseCommand
from django.conf import settings

import requests
from car_robot.scrapers import *
from utils.logging import logger


PAGE_URL = 'https://divar.ir/s/tehran/car/samand/lx/ef7-petrol'

cookies = {
    "_ga":          "GA1.2.1067222960.1693316377",
    "_gat":         "1",
    "_gid":         "GA1.2.1986902769.1703688618",
    "chat_opened":  "",
    "city":         "tehran",
    "did":          "136aa051-7d3c-450b-a8be-34865f59e1fb",
    "FEATURE_FLAG": "{\"flags\":{\"TEST1\":{\"name\":\"TEST1\",\"bool_value\":false},\"search_page_empty_state_web_server_side_enabled\":{\"name\":\"search_page_empty_state_web_server_side_enabled\",\"bool_value\":false}},\"evaluatedAt\":\"2023-12-29T07:21:33.261030540Z\",\"maximumCacheUsageSecondsOnError\":86400,\"minimumRefetchIntervalSeconds\":3600,\"expireDate\":1703838093271}",
    "multi-city":   "tehran|",
    "sessionid":    "",
    "token":        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMDkzNTg1Nzg0MTkiLCJpc3MiOiJhdXRoIiwidmVyaWZpZWRfdGltZSI6MTcwMzUxODQ0MiwiaWF0IjoxNzAzNTE4NDQyLCJleHAiOjE3MDg3MDI0NDIsInVzZXItdHlwZSI6InBlcnNvbmFsIiwidXNlci10eXBlLWZhIjoiXHUwNjdlXHUwNjQ2XHUwNjQ0IFx1MDYzNFx1MDYyZVx1MDYzNVx1MDZjYyIsInNpZCI6ImQ4NGE4Yjk3LTQ3YzgtNGJlMC1hMmM0LWVlZTZkZmU1OTc2NCJ9.mC3Zmg9u0tk2jwtTMBPWJ-n-NJQBSmcYJKYZsI1rjyc"
}


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
    res = requests.post(url, json=filters, cookies=cookies)
    data = res.json()
    return get_links(data)


class Command(BaseCommand):

    def handle(self, *args, **options):
        page = 2
        all_links = []

        with open('old_pages.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_links = data['all_links']

        if len(all_links) == 0:
            while True:
                print('-' * 100)
                print(f'{page = }')
                links = send_request(page)
                if len(links) == 0:
                    break
                all_links.extend(links)
                time.sleep(2)
                page += 1
            with open('old_pages.json', 'w', encoding='utf-8') as f:
                d = {'all_links': all_links}
                json.dump(d, f)

        robot = CarDetailScraper(all_links)
        robot.run()
