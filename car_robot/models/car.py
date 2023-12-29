from django.db import models


__all__ = [
    'Car'
]


class Car(models.Model):
    class Status(models.TextChoices):
        CALL_WAIT = 'CALL_WAIT'
        NO_ANSWER = 'NO_ANSWER'
        TALKED = 'TALKED'
        SOLD = 'SOLD'

    class SellerTypes(models.TextChoices):
        GREEDY = 'GREEDY'
        OK = 'OK'
        NA = 'NA'

    token = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    time = models.CharField(max_length=50)
    location = models.CharField(max_length=50, blank=True)
    kilometer = models.PositiveBigIntegerField()
    year = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=50)
    ad_type = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    fuel = models.CharField(max_length=50, blank=True)
    engine = models.CharField(max_length=50, blank=True)
    chassis = models.CharField(max_length=50, blank=True)
    chassis_front = models.CharField(max_length=50, blank=True)
    chassis_back = models.CharField(max_length=50, blank=True)
    body = models.CharField(max_length=50, blank=True)
    insurance = models.CharField(max_length=50, blank=True)
    gearbox = models.CharField(max_length=50, blank=True)
    can_exchange = models.CharField(max_length=50, blank=True)
    price = models.PositiveBigIntegerField()
    phone = models.CharField(max_length=15)
    description = models.TextField(default='')
    appointment = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CALL_WAIT, blank=True)
    seller_type = models.CharField(max_length=20, choices=SellerTypes.choices, default=SellerTypes.NA, blank=True)
    my_description = models.TextField(default='', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
