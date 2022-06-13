from django.db import models


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
    amount = models.BigIntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.type}-{self.amount}'


class Income(TimestampedModel):
    amount = models.BigIntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.amount}-{self.date}'


class ProductCost(TimestampedModel):
    amount = models.BigIntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.amount}-{self.date}'


class Invoice(models.Model):
    number = models.BigIntegerField(unique=True)
    start_date_persian = models.CharField(max_length=255)
    end_date_persian = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name='invoice_items'
    )

    row_number = models.IntegerField()
    code = models.BigIntegerField()

    date_persian = models.CharField(max_length=255)
    date = models.DateTimeField(blank=True, null=True)

    dkpc = models.BigIntegerField()
    variant_title = models.CharField(max_length=255)
    order_id = models.BigIntegerField()
    serial = models.CharField(max_length=255)
    credit = models.BigIntegerField()
    debit = models.BigIntegerField()
    credit_discount = models.BigIntegerField()
    debit_discount = models.BigIntegerField()
    credit_final = models.BigIntegerField()
    debit_final = models.BigIntegerField()
    description = models.TextField(blank=True, null=True)
    calculated = models.BooleanField(default=False)


__all__ = [
    'CostType',
    'Cost',
    'Income',
    'ProductCost',
    'Invoice',
    'InvoiceItem'
]
