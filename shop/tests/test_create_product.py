import json

from rest_framework.test import APIClient, APITransactionTestCase
from django.urls import reverse

from shop.models import *
from users.models import User


class TestProduct(APITransactionTestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.url_base = reverse('shop_api:products-list')

        self.user = User.objects.create_superuser(mobile='09125544666', password='123456')
        self.client.force_login(self.user)

        self.brand = Brand.objects.create(title='brand 1')
        self.selector_type = VariantSelectorType.objects.create(title='selector type 1')
        self.attribute_1 = ProductAttribute.objects.create(title='تعداد طبقه')
        self.attribute_2 = ProductAttribute.objects.create(title='ارتفاع')
        self.category = ProductCategory.objects.create(
            title='category 1',
            selector_type=self.selector_type,
            depth=0,
        )
        ProductCategoryAttribute.objects.create(category=self.category, attribute=self.attribute_1)
        ProductCategoryAttribute.objects.create(category=self.category, attribute=self.attribute_2)

    def test_1_create_product(self):
        payload = {
            'brand':            self.brand.id,
            'title':            '16 اینج',
            'category':         self.category.id,
            'is_active':        False,
            'attribute_values': [
                {
                    'attribute': self.attribute_1.id,
                    'value':     '3'
                },
                {
                    'attribute': self.attribute_2.id,
                    'value':     '20 cm'
                }
            ]
        }
        response = self.client.post(self.url_base, data=payload, format='json')
        print(response.status_code)
        data = response.data
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 201)
        self.product = Product.objects.first()
