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
        self.selector_type = SelectorType.objects.create(title='selector type 1')
        self.attribute_1 = Attribute.objects.create(title='تعداد طبقه')
        self.attribute_2 = Attribute.objects.create(title='ارتفاع')
        self.category = Category.objects.create(
            title='category 1',
            selector_type=self.selector_type,
            depth=0,
        )
        CategoryAttribute.objects.create(category=self.category, attribute=self.attribute_1)
        CategoryAttribute.objects.create(category=self.category, attribute=self.attribute_2)
        self.selector_1 = SelectorValue.objects.create(type=self.selector_type, title='مشکلی', value='#000')
        self.selector_2 = SelectorValue.objects.create(type=self.selector_type, title='سفید', value='#fff')

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
            ],
            'new_images':       [
                {'file': '/media/test1.jpg/', 'is_main': False},
                {'file': '/media/test2.jpg/', 'is_main': True},
            ],
            'main_img':         None,
        }
        response = self.client.post(self.url_base, data=payload, format='json')
        print(response.status_code)
        data = response.data
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, 201)

        # Adding Variants:
        payload = [
            {
                'product':        data['id'],
                'selector_value': self.selector_1.id,
                'is_active':      True,
                'price':          100000,
                'max_in_order':   4,
                'inventory':      10,
            }, {
                'product':        data['id'],
                'selector_value': self.selector_2.id,
                'is_active':      False,
                'price':          120000,
                'max_in_order':   3,
                'inventory':      15,
            },
        ]
        print('ggg:', f'{self.url_base}add-variants/')
        response = self.client.post(f'{self.url_base}add-variants/', data=payload, format='json')
        data = response.data
        print(json.dumps(data, indent=4))
