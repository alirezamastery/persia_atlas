from pprint import pprint

from django.core.management import BaseCommand

import requests
from car_robot.models import *


jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2NDQzOTc2LCJpYXQiOjE3MDM4NTE5NzYsImp0aSI6ImViMmE5NzEzNDA0NTQwYjU4OWYyMmMwOGM3NTMwNDFmIiwidXNlcl9pZCI6MX0.Wcg22IidzuCRfw0SVqtdD0ziA6eyVoDLtaRy9fYMgA0'


class Command(BaseCommand):

    def handle(self, *args, **options):
        cars = Car.objects.all().order_by('-id')
        url = 'https://persia-atlas.com/api/car-robot/cars/'
        headers = {
            'Authorization': f'Bearer {jwt}'
        }
        for car in cars:
            payload = {
                'token':          car.token,
                'title':          car.title,
                'time':           car.time,
                'location':       car.location,
                'kilometer':      car.kilometer,
                'year':           car.year,
                'color':          car.color,
                'ad_type':        car.ad_type,
                'model':          car.model,
                'fuel':           car.fuel,
                'engine':         car.engine,
                'chassis':        car.chassis,
                'chassis_front':  car.chassis_front,
                'chassis_back':   car.chassis_back,
                'body':           car.body,
                'insurance':      car.insurance,
                'gearbox':        car.gearbox,
                'can_exchange':   car.can_exchange,
                'price':          car.price,
                'phone':          car.phone,
                'description':    car.description,
                'appointment':    car.appointment,
                'status':         car.status,
                'seller_type':    car.seller_type,
                'my_description': car.my_description,
            }

            res = requests.post(url, json=payload, headers=headers)

            pprint(res.json())
            print(res.status_code)
