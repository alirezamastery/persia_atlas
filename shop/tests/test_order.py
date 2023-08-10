import json
from collections import OrderedDict
from pprint import pprint
from rest_framework.test import APIClient, APITransactionTestCase, APITestCase
from django.urls import reverse

from shop.models import *
from users.models import User


class TestOrder(APITestCase):
    fixtures = [
        'shop/tests/fixtures/create_order.json'
    ]

    def setUp(self) -> None:
        self.client = APIClient()
        self.url_base = reverse('shop_api:orders-list')

        self.user = User.objects.create_superuser(mobile='09125544666', password='123456')
        self.client.force_login(self.user)

        self.category = Category.objects.first()

    def test_1_create_order(self):
        payload = {
            'user':  self.user.id,
            'items': [
                {'variant': 2, 'quantity': 2},
                {'variant': 4, 'quantity': 4},
                {'variant': 5, 'quantity': 1},
            ],
        }
        response = self.client.post(f'{self.url_base}', data=payload, format='json')
        data = response.data
        print(json.dumps(data, indent=4))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['price_sum'], 1750000)

    def test_2_get_orders(self):
        payload = {
            'user':  self.user.id,
            'items': [
                {'variant': 2, 'quantity': 2},
                {'variant': 4, 'quantity': 4},
                {'variant': 5, 'quantity': 1},
            ],
        }
        self.client.post(f'{self.url_base}', data=payload, format='json')
        response = self.client.get(f'{self.url_base}', format='json')
        self.assertEqual(response.status_code, 200)
        data = response.data
        print(json.dumps(data, indent=4))
