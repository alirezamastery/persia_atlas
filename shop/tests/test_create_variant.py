import json

from rest_framework.test import APIClient, APITransactionTestCase
from django.urls import reverse

from shop.models import *
from users.models import User


class TestVariant(APITransactionTestCase):
    fixtures = [
        'shop/tests/fixtures/create_variant.json'
    ]

    def setUp(self) -> None:
        self.client = APIClient()
        self.url_base = reverse('shop_api:variants-list')

        self.user = User.objects.create_superuser(mobile='09125544666', password='123456')
        self.client.force_login(self.user)

    def test_1_create_variant(self):
        payload = {
            'product':        1,
            'selector_value': 1,
            'price':          1_000_000
        }
        response = self.client.post(self.url_base, data=payload, format='json')
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 201)
