import json
from pprint import pprint
from rest_framework.test import APIClient, APITransactionTestCase
from django.urls import reverse

from shop.models import *
from users.models import User


class TestCategory(APITransactionTestCase):
    fixtures = [
        'shop/tests/fixtures/category.json'
    ]

    def setUp(self) -> None:
        self.client = APIClient()
        self.url_base = reverse('shop_api:categories_admin-list')

        self.user = User.objects.create_superuser(mobile='09125544666', password='123456')
        self.client.force_login(self.user)

        self.category = ProductCategory.objects.first()

    def test_1_get_category(self):
        response = self.client.get(f'{self.url_base}{self.category.id}/')
        print(response.status_code)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 200)

    def test_2_update_category_title(self):
        payload = {
            'title': 'new title',
        }
        response = self.client.patch(f'{self.url_base}{self.category.id}/', data=payload, format='json')
        print(response.status_code)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'new title')

    def test_3_update_category_attributes(self):
        payload = {
            'attributes': [3, 4],
        }
        response = self.client.patch(f'{self.url_base}{self.category.id}/', data=payload, format='json')
        print(json.dumps(response.data, indent=4))

        category_id = response.data['id']
        correct_attr_ids = {1, 2, 3, 4}
        category_attrs = ProductCategoryAttribute.objects.filter(category_id=category_id)
        self.assertEqual(category_attrs.count(), 4)
        category_attr_ids = set([attr.attribute_id for attr in category_attrs])
        self.assertEqual(category_attr_ids, correct_attr_ids)

        products = Product.objects.filter(category_id=category_id)
        for product in products:
            product_attrs = ProductAttributeValue.objects.filter(product=product)
            product_attr_ids = set([attr.attribute_id for attr in product_attrs])
            self.assertEqual(product_attr_ids, correct_attr_ids)
