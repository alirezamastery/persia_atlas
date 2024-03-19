import time
import json

import requests
from django.core.management import BaseCommand

from car_robot.scrapers.laptop_detail import LaptopDetailScraper
from car_robot.scrapers.laptop_html_list import LaptopFirstPageListScraper


QUERY = 'tuf'


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
            "brands":              {
                "value": [
                    "Asus - ایسوس"
                ]
            },
            "category":            {
                "value": "laptops"
            },
            "goods-business-type": {
                "value": "personal"
            },
            "price":               {
                "min": 40000000
            },
            "processor":           {
                "value": [
                    "Core i7",
                    "Core i9",
                    "Ryzen 7"
                ]
            }
        },
        # "last-post-date": 1703743376247506,
        "page":        page
    }


def send_request(page: int):
    url = 'https://api.divar.ir/v8/web-search/1/laptops'
    filters = get_payload(page)
    res = requests.post(url, json=filters)
    data = res.json()
    return get_links(data)


class Command(BaseCommand):

    def handle(self, *args, **options):
        all_links = []

        # url = f'https://divar.ir/s/tehran/laptop-notebook-macbook?sort=most_expensive&goods-business-type=all&q={QUERY}'
        # url = f'https://divar.ir/s/tehran/laptop-notebook-macbook?sort=%DA%AF%D8%B1%D8%A7%D9%86%E2%80%8C%D8%AA%D8%B1%DB%8C%D9%86&goods-business-type=all&q={QUERY}'
        url = f'https://divar.ir/s/tehran/laptop-notebook-macbook/asus?goods-business-type=personal&price=40000000-&processor=Core%20i7%2CCore%20i9%2CRyzen%207'
        first_page_scraper = LaptopFirstPageListScraper(url)
        first_page_links = first_page_scraper.run()
        first_page_scraper.browser.quit()
        all_links.extend(first_page_links)

        page = 1
        api_links = []
        while True:
            print('-' * 100)
            print(f'{page = }')
            links = send_request(page)
            if len(links) == 0:
                break
            api_links.extend(links)
            time.sleep(2)
            page += 1

        all_links.extend(api_links)
        print(len(all_links))

        robot = LaptopDetailScraper(all_links)
        robot.run()
        robot.browser.quit()
