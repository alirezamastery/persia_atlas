from rest_framework.serializers import ModelSerializer

from car_robot.models import *


__all__ = [
    'CarReadSerializer',
    'CarWriteSerializer',
]


class CarReadSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarWriteSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'token',
            'title',
            'time',
            'location',
            'kilometer',
            'year',
            'color',
            'ad_type',
            'model',
            'fuel',
            'engine',
            'chassis',
            'chassis_front',
            'chassis_back',
            'body',
            'insurance',
            'gearbox',
            'can_exchange',
            'price',
            'phone',
            'status',
            'description',
            'appointment',
            'seller_type',
            'my_description',
        ]
