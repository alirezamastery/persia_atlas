from django.db import models


__all__ = [
    'CostType', 'Cost', 'Income', 'ProductCost'
]


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CostType(TimestampedModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title}'


class Cost(TimestampedModel):
    type = models.ForeignKey(CostType, on_delete=models.PROTECT, related_name='costs')
    amount = models.IntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.type}-{self.amount}'


class Income(TimestampedModel):
    amount = models.IntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.amount}-{self.date}'


class ProductCost(TimestampedModel):
    amount = models.IntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.amount}-{self.date}'
